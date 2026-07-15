from __future__ import annotations

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .mediaserver import MediaServerRefresher
from .strm import StrmSyncService

logger = logging.getLogger(__name__)


class SyncScheduler:
    def __init__(self, sync_service: StrmSyncService, refresher: MediaServerRefresher):
        self.sync_service = sync_service
        self.refresher = refresher
        self.scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._lock = asyncio.Lock()
        self.last_result: dict | None = None
        self.running = False

    def start(self, full_cron: str, increment_cron: str) -> None:
        self.scheduler.add_job(
            self.run_sync,
            CronTrigger.from_crontab(full_cron, timezone="Asia/Shanghai"),
            id="full_sync",
            kwargs={"mode": "full", "refresh_media": True},
            replace_existing=True,
        )
        self.scheduler.add_job(
            self.run_sync,
            CronTrigger.from_crontab(increment_cron, timezone="Asia/Shanghai"),
            id="increment_sync",
            kwargs={"mode": "increment", "refresh_media": False},
            replace_existing=True,
        )
        self.scheduler.start()

    async def run_sync(
        self,
        dry_run: bool = False,
        mode: str = "increment",
        refresh_media: bool = True,
        path_indexes: list[int] | None = None,
    ) -> dict:
        if self._lock.locked():
            return {"running": True, "message": "sync already running"}

        async with self._lock:
            self.running = True
            loop = asyncio.get_running_loop()
            normalized_mode = mode if mode in {"full", "increment"} else "increment"
            force_overwrite = normalized_mode == "full"
            try:
                result = await loop.run_in_executor(
                    self.executor,
                    lambda: self.sync_service.sync_all(
                        dry_run=dry_run,
                        force_overwrite=force_overwrite,
                        selected_path_indexes=path_indexes,
                    ),
                )
                refresh_ok = await self.refresher.refresh() if refresh_media else None
                data = {
                    "running": False,
                    "dry_run": dry_run,
                    "mode": normalized_mode,
                    "force_overwrite": force_overwrite,
                    "path_indexes": path_indexes,
                    "scanned": result.scanned,
                    "written": result.written,
                    "skipped": result.skipped,
                    "failed": result.failed,
                    "limited": result.limited,
                    "refresh_requested": refresh_media,
                    "media_refresh": refresh_ok,
                }
                self.last_result = data
                logger.info("sync complete: %s", data)
                return data
            finally:
                self.running = False

    async def refresh_media_server(self) -> dict:
        refresh_ok = await self.refresher.refresh()
        return {"enabled": self.refresher.config.enabled, "media_refresh": refresh_ok}

    def status(self) -> dict:
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "next_run_time": job.next_run_time.isoformat()
                    if job.next_run_time
                    else None,
                }
            )
        return {
            "running": self.running,
            "jobs": jobs,
            "last_result": self.last_result,
        }

    def shutdown(self) -> None:
        self.scheduler.shutdown(wait=False)
        self.executor.shutdown(wait=False, cancel_futures=True)
