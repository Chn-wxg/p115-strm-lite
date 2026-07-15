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

    def start(self, full_cron: str, increment_cron: str) -> None:
        self.scheduler.add_job(
            self.run_sync,
            CronTrigger.from_crontab(full_cron, timezone="Asia/Shanghai"),
            id="full_sync",
            replace_existing=True,
        )
        self.scheduler.add_job(
            self.run_sync,
            CronTrigger.from_crontab(increment_cron, timezone="Asia/Shanghai"),
            id="increment_sync",
            replace_existing=True,
        )
        self.scheduler.start()

    async def run_sync(self, dry_run: bool = False) -> dict:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            self.executor,
            lambda: self.sync_service.sync_all(dry_run=dry_run),
        )
        refresh_ok = await self.refresher.refresh()
        data = {
            "scanned": result.scanned,
            "written": result.written,
            "skipped": result.skipped,
            "failed": result.failed,
            "media_refresh": refresh_ok,
        }
        logger.info("sync complete: %s", data)
        return data

    def shutdown(self) -> None:
        self.scheduler.shutdown(wait=False)
        self.executor.shutdown(wait=False, cancel_futures=True)

