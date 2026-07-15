from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .config import AppConfig, SyncPath
from .p115 import P115Service, PanFile


@dataclass(slots=True)
class SyncResult:
    scanned: int = 0
    written: int = 0
    skipped: int = 0
    failed: int = 0
    limited: bool = False


class StrmSyncService:
    def __init__(self, config: AppConfig, p115: P115Service):
        self.config = config
        self.p115 = p115

    def sync_all(
        self,
        dry_run: bool = False,
        force_overwrite: bool = False,
    ) -> SyncResult:
        result = SyncResult()
        for item in self.config.sync.paths:
            partial = self.sync_path(
                item,
                dry_run=dry_run,
                force_overwrite=force_overwrite,
                remaining=self._remaining_limit(result),
            )
            result.scanned += partial.scanned
            result.written += partial.written
            result.skipped += partial.skipped
            result.failed += partial.failed
            result.limited = result.limited or partial.limited
            if self._limit_reached(result):
                result.limited = True
                break
        return result

    def sync_path(
        self,
        sync_path: SyncPath,
        dry_run: bool = False,
        force_overwrite: bool = False,
        remaining: int | None = None,
    ) -> SyncResult:
        result = SyncResult()
        if remaining == 0:
            result.limited = True
            return result
        for pan_file in self.p115.iter_files(sync_path.pan_path):
            if self._limit_reached(result, remaining=remaining):
                result.limited = True
                break
            result.scanned += 1
            if not self._should_generate(pan_file):
                result.skipped += 1
                self._throttle(result)
                continue
            try:
                target = self._target_path(sync_path, pan_file)
                if (
                    target.exists()
                    and not force_overwrite
                    and not self.config.strm.overwrite
                ):
                    result.skipped += 1
                    self._throttle(result)
                    continue
                if not dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(
                        self._strm_content(pan_file),
                        encoding="utf-8",
                        newline="\n",
                    )
                result.written += 1
            except Exception:
                result.failed += 1
            self._throttle(result)
        return result

    def _limit_reached(self, result: SyncResult, remaining: int | None = None) -> bool:
        limit = self.config.sync.max_files_per_run if remaining is None else remaining
        return limit > 0 and result.scanned >= limit

    def _remaining_limit(self, result: SyncResult) -> int | None:
        limit = self.config.sync.max_files_per_run
        if limit <= 0:
            return None
        return max(0, limit - result.scanned)

    def _throttle(self, result: SyncResult) -> None:
        item_sleep = self.config.sync.item_sleep_seconds
        if item_sleep > 0:
            time.sleep(item_sleep)

        batch_size = self.config.sync.batch_size
        batch_sleep = self.config.sync.batch_sleep_seconds
        if batch_size > 0 and batch_sleep > 0 and result.scanned % batch_size == 0:
            time.sleep(batch_sleep)

    def _should_generate(self, pan_file: PanFile) -> bool:
        if pan_file.suffix not in self.config.strm.media_suffixes:
            return False
        return pan_file.size >= self.config.strm.min_file_size

    def _target_path(self, sync_path: SyncPath, pan_file: PanFile) -> Path:
        relative = PurePosixPath(pan_file.path).relative_to(
            PurePosixPath(sync_path.pan_path)
        )
        local = Path(sync_path.local_path) / Path(*relative.parts)
        return local.with_suffix(".strm")

    def _strm_content(self, pan_file: PanFile) -> str:
        base = self.config.server.public_url.rstrip("/")
        return f"{base}/redirect_url?pickcode={pan_file.pickcode}\n"
