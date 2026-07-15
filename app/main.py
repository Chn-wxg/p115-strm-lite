from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .config import load_config
from .mediaserver import MediaServerRefresher
from .p115 import P115Service
from .scheduler import SyncScheduler
from .strm import StrmSyncService
from .ui import PAGE_HTML

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

config = load_config()
p115_service = P115Service(config)
sync_service = StrmSyncService(config, p115_service)
refresher = MediaServerRefresher(config.media_server)
sync_scheduler = SyncScheduler(sync_service, refresher)

app = FastAPI(title="p115-strm-lite", version="0.1.0")


@app.on_event("startup")
async def startup() -> None:
    sync_scheduler.start(config.sync.full_cron, config.sync.increment_cron)


@app.on_event("shutdown")
async def shutdown() -> None:
    sync_scheduler.shutdown()


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return PAGE_HTML


@app.head("/")
async def index_head() -> dict:
    return {}


@app.get("/health")
async def health() -> dict:
    return {"ok": True}


@app.get("/api/status")
async def api_status() -> dict:
    return {
        "server": {"public_url": config.server.public_url},
        "auth": {"has_p115_cookies": bool(config.auth.p115_cookies)},
        "sync": {
            "full_cron": config.sync.full_cron,
            "increment_cron": config.sync.increment_cron,
            "max_files_per_run": config.sync.max_files_per_run,
            "batch_size": config.sync.batch_size,
            "batch_sleep_seconds": config.sync.batch_sleep_seconds,
            "item_sleep_seconds": config.sync.item_sleep_seconds,
            "paths": [
                {"pan_path": item.pan_path, "local_path": item.local_path}
                for item in config.sync.paths
            ],
        },
        "strm": {
            "media_ext": config.strm.media_ext,
            "subtitle_ext": config.strm.subtitle_ext,
            "overwrite": config.strm.overwrite,
            "min_file_size": config.strm.min_file_size,
        },
        "media_server": {
            "enabled": config.media_server.enabled,
            "type": config.media_server.type,
            "url": config.media_server.url,
        },
        "scheduler": sync_scheduler.status(),
    }


@app.post("/sync")
async def sync(
    dry_run: bool = False,
    mode: str = "increment",
    refresh_media: bool = True,
) -> dict:
    return await sync_scheduler.run_sync(
        dry_run=dry_run,
        mode=mode,
        refresh_media=refresh_media,
    )


@app.post("/api/media/refresh")
async def refresh_media() -> dict:
    return await sync_scheduler.refresh_media_server()


@app.get("/redirect_url")
async def redirect_url(pickcode: str, request: Request) -> RedirectResponse:
    if not pickcode:
        raise HTTPException(status_code=400, detail="pickcode is required")
    try:
        url = await p115_service.get_download_url(
            pickcode=pickcode,
            user_agent=request.headers.get("user-agent", ""),
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return RedirectResponse(url=url, status_code=302)
