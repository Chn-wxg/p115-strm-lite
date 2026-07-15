from __future__ import annotations

import asyncio

import httpx

from .config import MediaServerConfig


class MediaServerRefresher:
    def __init__(self, config: MediaServerConfig):
        self.config = config

    async def refresh(self) -> bool:
        if not self.config.enabled:
            return True
        if self.config.refresh_delay_seconds > 0:
            await asyncio.sleep(self.config.refresh_delay_seconds)
        if self.config.type.lower() == "emby":
            return await self._refresh_emby()
        if self.config.type.lower() == "jellyfin":
            return await self._refresh_jellyfin()
        raise ValueError(f"Unsupported media server type: {self.config.type}")

    async def _refresh_emby(self) -> bool:
        url = self.config.url.rstrip("/") + "/emby/Library/Refresh"
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(url, params={"api_key": self.config.api_key})
        resp.raise_for_status()
        return True

    async def _refresh_jellyfin(self) -> bool:
        url = self.config.url.rstrip("/") + "/Library/Refresh"
        headers = {"X-Emby-Token": self.config.api_key}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(url, headers=headers)
        resp.raise_for_status()
        return True

