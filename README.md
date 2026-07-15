# p115-strm-lite

轻量独立版 115 STRM 助手，用来替代 MoviePilot 插件中的基础 STRM 能力。

第一版目标：

- 读取 115 Cookie
- 扫描 115 网盘目录
- 生成 `.strm`
- 提供 `GET /redirect_url?pickcode=xxx` 播放重定向
- 定时全量/轻量增量同步
- 可选刷新 Emby/Jellyfin 媒体库

## 快速开始

复制配置：

```bash
mkdir -p config
cp config.example.yaml config/config.yaml
```

编辑 `config/config.yaml`：

- `auth.p115_cookies`
- `server.public_url`
- `sync.paths`
- `media_server`

启动：

```bash
docker compose up -d
```

也可以直接拉取镜像：

```bash
docker pull ghcr.io/chn-wxg/p115-strm-lite:latest
```

健康检查：

```bash
curl http://127.0.0.1:18080/health
```

手动同步：

```bash
curl -X POST "http://127.0.0.1:18080/sync?dry_run=true"
curl -X POST "http://127.0.0.1:18080/sync"
```

## STRM 内容

生成的 STRM 内容形如：

```text
http://你的FNOS_IP:18080/redirect_url?pickcode=xxxx
```

播放时服务会用 115 Cookie 换取真实下载地址并返回 302。

## 路径说明

`sync.paths` 中：

```yaml
sync:
  paths:
    - pan_path: "/电影"
      local_path: "/media/电影"
```

表示扫描 115 网盘 `/电影`，把 STRM 生成到容器内 `/media/电影`。

Docker Compose 里需要把 FNOS 的媒体目录挂载到容器 `/media`。
