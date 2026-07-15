from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG_PATH = Path(os.environ.get("P115_STRM_CONFIG", "/config/config.yaml"))


DEFAULT_CONFIG_TEXT = """server:
  public_url: "http://127.0.0.1:18080"

auth:
  p115_cookies: "UID=xxx; CID=xxx; SEID=xxx"

strm:
  media_ext:
    - mp4
    - mkv
    - ts
    - iso
    - rmvb
    - avi
    - mov
    - mpeg
    - mpg
    - wmv
    - m4v
    - flv
    - m2ts
  subtitle_ext:
    - srt
    - ass
    - ssa
  overwrite: false
  min_file_size: 0

sync:
  full_cron: "0 3 * * *"
  increment_cron: "*/30 * * * *"
  max_files_per_run: 5000
  batch_size: 500
  batch_sleep_seconds: 2
  item_sleep_seconds: 0
  paths:
    - pan_path: "/strm"
      local_path: "/media"

media_server:
  enabled: false
  type: "emby"
  url: "http://127.0.0.1:8096"
  api_key: ""
  refresh_delay_seconds: 0
"""


@dataclass(slots=True)
class ServerConfig:
    public_url: str = "http://127.0.0.1:18080"


@dataclass(slots=True)
class AuthConfig:
    p115_cookies: str = ""


@dataclass(slots=True)
class StrmConfig:
    media_ext: list[str] = field(
        default_factory=lambda: [
            "mp4",
            "mkv",
            "ts",
            "iso",
            "rmvb",
            "avi",
            "mov",
            "mpeg",
            "mpg",
            "wmv",
            "m4v",
            "flv",
            "m2ts",
        ]
    )
    subtitle_ext: list[str] = field(default_factory=lambda: ["srt", "ass", "ssa"])
    overwrite: bool = False
    min_file_size: int = 0

    @property
    def media_suffixes(self) -> set[str]:
        return {f".{ext.lower().lstrip('.')}" for ext in self.media_ext}

    @property
    def subtitle_suffixes(self) -> set[str]:
        return {f".{ext.lower().lstrip('.')}" for ext in self.subtitle_ext}


@dataclass(slots=True)
class SyncPath:
    pan_path: str
    local_path: str


@dataclass(slots=True)
class SyncConfig:
    full_cron: str = "0 3 * * *"
    increment_cron: str = "*/30 * * * *"
    max_files_per_run: int = 5000
    batch_size: int = 500
    batch_sleep_seconds: float = 2.0
    item_sleep_seconds: float = 0.0
    paths: list[SyncPath] = field(default_factory=list)


@dataclass(slots=True)
class MediaServerConfig:
    enabled: bool = False
    type: str = "emby"
    url: str = ""
    api_key: str = ""
    refresh_delay_seconds: int = 0


@dataclass(slots=True)
class AppConfig:
    server: ServerConfig = field(default_factory=ServerConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    strm: StrmConfig = field(default_factory=StrmConfig)
    sync: SyncConfig = field(default_factory=SyncConfig)
    media_server: MediaServerConfig = field(default_factory=MediaServerConfig)


def _section(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key) or {}
    if not isinstance(value, dict):
        raise ValueError(f"Config section {key!r} must be an object")
    return value


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(DEFAULT_CONFIG_TEXT, encoding="utf-8", newline="\n")

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("Config root must be an object")

    sync_raw = _section(raw, "sync")
    paths = [
        SyncPath(
            pan_path=str(item["pan_path"]).rstrip("/") or "/",
            local_path=str(item["local_path"]),
        )
        for item in sync_raw.get("paths", [])
        if isinstance(item, dict) and item.get("pan_path") and item.get("local_path")
    ]

    return AppConfig(
        server=ServerConfig(**_section(raw, "server")),
        auth=AuthConfig(**_section(raw, "auth")),
        strm=StrmConfig(**_section(raw, "strm")),
        sync=SyncConfig(
            full_cron=str(sync_raw.get("full_cron", "0 3 * * *")),
            increment_cron=str(sync_raw.get("increment_cron", "*/30 * * * *")),
            max_files_per_run=max(0, int(sync_raw.get("max_files_per_run", 5000))),
            batch_size=max(0, int(sync_raw.get("batch_size", 500))),
            batch_sleep_seconds=max(
                0.0, float(sync_raw.get("batch_sleep_seconds", 2.0))
            ),
            item_sleep_seconds=max(0.0, float(sync_raw.get("item_sleep_seconds", 0.0))),
            paths=paths,
        ),
        media_server=MediaServerConfig(**_section(raw, "media_server")),
    )
