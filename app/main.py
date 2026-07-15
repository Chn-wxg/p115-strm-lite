from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from .config import load_config
from .mediaserver import MediaServerRefresher
from .p115 import P115Service
from .scheduler import SyncScheduler
from .strm import StrmSyncService

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


@app.get("/health")
async def health() -> dict:
    return {"ok": True}


@app.post("/sync")
async def sync(dry_run: bool = False) -> dict:
    return await sync_scheduler.run_sync(dry_run=dry_run)


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

