from __future__ import annotations

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


class StrmSyncService:
    def __init__(self, config: AppConfig, p115: P115Service):
        self.config = config
        self.p115 = p115

    def sync_all(self, dry_run: bool = False) -> SyncResult:
        result = SyncResult()
        for item in self.config.sync.paths:
            partial = self.sync_path(item, dry_run=dry_run)
            result.scanned += partial.scanned
            result.written += partial.written
            result.skipped += partial.skipped
            result.failed += partial.failed
        return result

    def sync_path(self, sync_path: SyncPath, dry_run: bool = False) -> SyncResult:
        result = SyncResult()
        for pan_file in self.p115.iter_files(sync_path.pan_path):
            result.scanned += 1
            if not self._should_generate(pan_file):
                result.skipped += 1
                continue
            try:
                target = self._target_path(sync_path, pan_file)
                if target.exists() and not self.config.strm.overwrite:
                    result.skipped += 1
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
        return result

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

