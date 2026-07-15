from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable
from urllib.parse import parse_qsl, unquote, urlsplit

import httpx
import orjson
from p115client import P115Client, check_response
from p115client.tool.iterdir import iter_files_with_path_skim
from p115rsacipher import decrypt, encrypt

from .config import AppConfig
from .cookies import parse_cookie_header


@dataclass(slots=True)
class PanFile:
    id: int
    parent_id: int
    name: str
    path: str
    pickcode: str
    sha1: str
    size: int

    @property
    def suffix(self) -> str:
        return PurePosixPath(self.name).suffix.lower()


class P115Service:
    def __init__(self, config: AppConfig):
        if not config.auth.p115_cookies:
            raise ValueError("auth.p115_cookies is required")
        self.config = config
        self.client = P115Client(config.auth.p115_cookies)
        self._download_cache: dict[tuple[str, str], tuple[str, float]] = {}

    def get_dir_id(self, pan_path: str) -> int:
        if pan_path == "/":
            return 0
        resp = self.client.fs_dir_getid(pan_path, app="ios")
        check_response(resp)
        dir_id = int(resp.get("id", -1))
        if dir_id < 0:
            raise FileNotFoundError(f"115 directory not found: {pan_path}")
        return dir_id

    def iter_files(self, pan_path: str) -> Iterable[PanFile]:
        dir_id = self.get_dir_id(pan_path)
        for item in iter_files_with_path_skim(
            self.client,
            cid=dir_id,
            with_ancestors=True,
            app="ios",
        ):
            name = item.get("name") or item.get("n") or ""
            path = item.get("path") or self._build_path(item, pan_path, name)
            pickcode = item.get("pickcode") or item.get("pick_code") or item.get("pc")
            if not name or not pickcode:
                continue
            yield PanFile(
                id=int(item.get("id") or item.get("fid") or 0),
                parent_id=int(item.get("parent_id") or item.get("pid") or 0),
                name=str(name),
                path=str(path),
                pickcode=str(pickcode),
                sha1=str(item.get("sha1") or ""),
                size=int(item.get("size") or item.get("fs") or 0),
            )

    @staticmethod
    def _build_path(item: dict, pan_path: str, name: str) -> str:
        ancestors = item.get("ancestors") or []
        names = [a.get("name") for a in ancestors[1:] if a.get("name")]
        if names:
            return "/" + "/".join([*names, name])
        return f"{pan_path.rstrip('/')}/{name}"

    async def get_download_url(self, pickcode: str, user_agent: str = "") -> str:
        cache_key = (pickcode, user_agent or "NoUA")
        cached = self._download_cache.get(cache_key)
        if cached and cached[1] > time.time():
            return cached[0]

        headers = {"User-Agent": user_agent} if user_agent else {}
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(15.0, connect=8.0),
            cookies=parse_cookie_header(self.config.auth.p115_cookies),
        ) as client:
            resp = await client.post(
                "http://proapi.115.com/android/2.0/ufile/download",
                data={
                    "data": encrypt(f'{{"pick_code":"{pickcode}"}}').decode("utf-8")
                },
                headers=headers,
            )
        resp.raise_for_status()
        payload = orjson.loads(resp.content)
        if not payload.get("state"):
            raise RuntimeError(f"115 download url request failed: {payload}")
        data = orjson.loads(decrypt(payload["data"]))
        url = data["url"]
        expires_at = self._extract_expiry(url)
        self._download_cache[cache_key] = (url, expires_at)
        return url

    @staticmethod
    def _extract_expiry(url: str) -> float:
        try:
            expire = int(next(v for k, v in parse_qsl(urlsplit(url).query) if k == "t"))
            return max(time.time(), expire - 300)
        except Exception:
            return time.time() + 600

    @staticmethod
    def filename_from_url(url: str) -> str:
        return unquote(urlsplit(url).path.rpartition("/")[-1])

