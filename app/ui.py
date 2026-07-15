from __future__ import annotations


PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>115网盘STRM助手</title>
  <style>
    :root {
      --bg: #f7fbff;
      --panel: #ffffff;
      --line: #e5e7eb;
      --line-strong: #d6d9e0;
      --text: #374151;
      --muted: #8a8f99;
      --purple: #8b5cf6;
      --blue: #0ea5e9;
      --green: #52c41a;
      --orange: #f59e0b;
      --red: #ff4d4f;
      --cyan-soft: #e6f7ff;
      --yellow-soft: #fff7e6;
      --shadow: 0 8px 22px rgba(15, 23, 42, .08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background:
        linear-gradient(115deg, rgba(224, 247, 255, .9), rgba(255, 239, 246, .68) 46%, rgba(255, 255, 255, .96) 72%),
        var(--bg);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
    }
    header {
      height: 38px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 16px;
      color: #6b7280;
      background: rgba(255, 255, 255, .55);
      border-bottom: 1px solid rgba(214, 219, 229, .8);
      font-weight: 700;
    }
    main { padding: 12px 12px 72px; }
    .layout {
      display: grid;
      grid-template-columns: minmax(340px, 1fr) minmax(360px, 1fr);
      gap: 24px;
      align-items: start;
    }
    .stack { display: grid; gap: 16px; }
    .card {
      background: rgba(255, 255, 255, .82);
      border: 1px solid var(--line-strong);
      border-radius: 14px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .card-title {
      height: 34px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0 18px;
      background: linear-gradient(110deg, rgba(219, 242, 255, .85), rgba(255, 239, 246, .76));
      color: #6b7280;
      font-size: 15px;
      font-weight: 800;
    }
    .card-body { padding: 14px 18px; }
    .row {
      min-height: 38px;
      display: grid;
      grid-template-columns: 24px 1fr auto;
      gap: 10px;
      align-items: center;
      border-bottom: 1px solid rgba(229, 231, 235, .8);
    }
    .row:last-child { border-bottom: 0; }
    .icon { color: var(--purple); font-weight: 900; text-align: center; }
    .label { color: #6b7280; }
    .hint { color: var(--muted); font-size: 13px; margin-top: 3px; }
    .badge {
      min-width: 52px;
      min-height: 22px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 8px;
      border-radius: 999px;
      background: #eff6ff;
      color: var(--blue);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }
    .badge.green { background: #f0fdf4; color: var(--green); }
    .badge.orange { background: #fffbeb; color: var(--orange); }
    .badge.gray { background: #f3f4f6; color: #9ca3af; }
    .badge.red { background: #fff1f2; color: var(--red); }
    .user {
      display: grid;
      grid-template-columns: 44px 1fr auto;
      align-items: center;
      gap: 12px;
      min-height: 54px;
    }
    .avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: linear-gradient(135deg, #c4b5fd, #67e8f9);
      color: #fff;
      font-weight: 900;
    }
    .progress {
      height: 7px;
      border-radius: 999px;
      background: #ede9fe;
      overflow: hidden;
      margin-top: 8px;
    }
    .bar {
      width: 18%;
      height: 100%;
      background: linear-gradient(90deg, #8b5cf6, #38bdf8);
    }
    .path-block {
      display: grid;
      gap: 10px;
    }
    .path-pair {
      min-height: 56px;
      display: grid;
      grid-template-columns: 1fr 46px 1fr;
      gap: 10px;
      align-items: center;
      padding: 10px 14px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, .68);
    }
    .path-box {
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 8px;
      align-items: center;
      min-width: 0;
    }
    code {
      color: #6b7280;
      background: transparent;
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      word-break: break-all;
    }
    .switch-line {
      display: grid;
      grid-template-columns: repeat(3, minmax(180px, 1fr));
      gap: 18px;
      margin-bottom: 16px;
    }
    .switch {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #7b7f89;
      font-size: 15px;
    }
    .toggle {
      width: 38px;
      height: 20px;
      border-radius: 999px;
      background: #d1d5db;
      position: relative;
      flex: 0 0 auto;
    }
    .toggle::after {
      content: "";
      width: 18px;
      height: 18px;
      position: absolute;
      top: 1px;
      left: 1px;
      border-radius: 50%;
      background: #fff;
      box-shadow: 0 1px 4px rgba(0, 0, 0, .2);
    }
    .toggle.on { background: #38bdf8; }
    .toggle.on::after { left: 19px; }
    .notice {
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 8px;
      align-items: start;
      padding: 12px 16px;
      border-radius: 6px;
      background: var(--cyan-soft);
      color: #1890ff;
      margin-bottom: 16px;
      line-height: 1.6;
    }
    .notice.warn {
      background: var(--yellow-soft);
      color: #d48806;
    }
    .tabs {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border-bottom: 1px solid var(--line);
    }
    .tab {
      height: 42px;
      display: grid;
      place-items: center;
      color: #777985;
      font-weight: 700;
    }
    .tab.active {
      color: var(--purple);
      border-bottom: 2px solid var(--purple);
    }
    .result {
      min-height: 132px;
      max-height: 260px;
      overflow: auto;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #111827;
      color: #e5e7eb;
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 13px;
      line-height: 1.5;
      white-space: pre-wrap;
    }
    .dock {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      min-height: 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 7px 12px;
      background: rgba(255, 255, 255, .92);
      border-top: 1px solid var(--line-strong);
      box-shadow: 0 -8px 20px rgba(15, 23, 42, .08);
    }
    .dock .left, .dock .right { display: flex; flex-wrap: wrap; gap: 10px; }
    button {
      min-height: 34px;
      border: 0;
      border-radius: 7px;
      padding: 0 12px;
      background: transparent;
      color: #7c3aed;
      font-weight: 800;
      cursor: pointer;
    }
    button.primary { color: var(--orange); }
    button.save { color: var(--green); }
    button.danger { color: var(--red); }
    button:disabled { color: #a8a8b0; cursor: not-allowed; }
    @media (max-width: 920px) {
      .layout { grid-template-columns: 1fr; }
      .switch-line { grid-template-columns: 1fr; }
      .tabs { grid-template-columns: repeat(2, 1fr); }
    }
  </style>
</head>
<body>
  <header>
    <span class="icon">STRM</span>
    <span>115网盘STRM助手</span>
  </header>

  <main>
    <section class="layout">
      <div class="stack">
        <article class="card">
          <div class="card-title">系统状态</div>
          <div class="card-body">
            <div class="row">
              <span class="icon">P</span><span class="label">插件状态</span><span id="pluginState" class="badge green">已启用</span>
            </div>
            <div class="row">
              <span class="icon">C</span><span class="label">115 Cookie 状态</span><span id="cookieState" class="badge gray">读取中</span>
            </div>
            <div class="row">
              <span class="icon">T</span><span class="label">任务状态</span><span id="taskState" class="badge orange">读取中</span>
            </div>
          </div>
        </article>

        <article class="card">
          <div class="card-title">115账户信息</div>
          <div class="card-body">
            <div class="user">
              <div class="avatar">115</div>
              <div>
                <div id="accountName">匿名用户</div>
                <div class="hint" id="cookieHint">Cookie 仅用于容器内请求，不会在页面显示明文</div>
              </div>
              <span id="vipState" class="badge gray">未检测</span>
            </div>
            <div class="progress"><div class="bar"></div></div>
            <div class="hint">容量信息接口还没接，后续可以补成和 MP 一样的账号概览。</div>
          </div>
        </article>

        <article class="card">
          <div class="card-title">功能配置</div>
          <div class="card-body">
            <div class="row">
              <span class="icon">M</span><span class="label">监控 MP 整理</span><span class="badge gray">不适用</span>
            </div>
            <div class="row">
              <span class="icon">F</span><span class="label">定时全量同步</span><span id="fullCron" class="badge green">已启用</span>
            </div>
            <div class="row">
              <span class="icon">I</span><span class="label">定时增量同步</span><span id="incrementCron" class="badge green">已启用</span>
            </div>
            <div class="row">
              <span class="icon">S</span><span class="label">媒体服务器刷新</span><span id="mediaRefreshState" class="badge gray">读取中</span>
            </div>
            <div class="row">
              <span class="icon">Q</span><span class="label">扫码登录</span><span class="badge gray">暂未实现</span>
            </div>
          </div>
        </article>
      </div>

      <div class="stack">
        <article class="card">
          <div class="card-title">路径配置</div>
          <div class="card-body">
            <div class="hint">同步路径映射</div>
            <div id="paths" class="path-block"></div>
          </div>
        </article>

        <article class="card">
          <div class="tabs">
            <div class="tab active">STRM同步</div>
            <div class="tab">网盘管理</div>
            <div class="tab">其他功能</div>
            <div class="tab">系统配置</div>
          </div>
          <div class="card-body">
            <div class="notice">
              <strong>i</strong>
              <div>当前独立版负责扫描 115 网盘目录，并在本地目录生成 STRM 文件。配置修改仍通过 <code>config.yaml</code> 完成。</div>
            </div>
            <div class="switch-line">
              <div class="switch"><span class="toggle on"></span><span>启用</span></div>
              <div class="switch"><span class="toggle" id="mediaToggle"></span><span>媒体服务器刷新</span></div>
              <div class="switch"><span class="toggle"></span><span>STRM 自动刮削</span></div>
            </div>
            <div class="notice warn">
              <strong>!</strong>
              <div>清理失效 STRM、扫码登录、在线编辑配置还没有接入；先把同步和播放链路跑稳，再补这些重功能。</div>
            </div>
            <div class="result" id="result">等待操作...</div>
          </div>
        </article>
      </div>
    </section>
  </main>

  <footer class="dock">
    <div class="left">
      <button id="reload">刷新状态</button>
    </div>
    <div class="right">
      <button id="dry">干跑预览</button>
      <button id="refresh">刷新媒体库</button>
      <button class="primary" id="sync">全量同步</button>
      <button class="save" id="save" disabled>保存配置</button>
      <button class="danger" disabled>关闭</button>
    </div>
  </footer>

  <script>
    const $ = (id) => document.getElementById(id);
    const buttons = [...document.querySelectorAll("button:not([disabled])")];

    function show(data) {
      $("result").textContent = JSON.stringify(data, null, 2);
    }

    function setBusy(busy) {
      buttons.forEach((button) => button.disabled = busy);
    }

    async function api(path, options = {}) {
      const response = await fetch(path, options);
      const data = await response.json();
      if (!response.ok) throw data;
      return data;
    }

    function badge(el, text, kind) {
      el.textContent = text;
      el.className = "badge " + kind;
    }

    function render(data) {
      badge($("cookieState"), data.auth.has_p115_cookies ? "已连接" : "未配置", data.auth.has_p115_cookies ? "green" : "red");
      badge($("taskState"), data.scheduler.running ? "运行中" : "空闲", data.scheduler.running ? "orange" : "green");
      badge($("mediaRefreshState"), data.media_server.enabled ? "已启用" : "已禁用", data.media_server.enabled ? "green" : "gray");
      $("mediaToggle").className = data.media_server.enabled ? "toggle on" : "toggle";
      $("fullCron").textContent = data.sync.full_cron || "未配置";
      $("incrementCron").textContent = data.sync.increment_cron || "未配置";
      $("accountName").textContent = data.auth.has_p115_cookies ? "Cookie 已配置" : "匿名用户";
      $("vipState").textContent = data.auth.has_p115_cookies ? "待检测" : "未登录";

      const paths = $("paths");
      paths.innerHTML = "";
      for (const item of data.sync.paths) {
        const div = document.createElement("div");
        div.className = "path-pair";
        div.innerHTML = `
          <div class="path-box"><span class="icon">L</span><div><div class="hint">本地目录</div><code>${item.local_path}</code></div></div>
          <div class="icon">SYNC</div>
          <div class="path-box"><span class="icon">P</span><div><div class="hint">网盘目录</div><code>${item.pan_path}</code></div></div>
        `;
        paths.appendChild(div);
      }
      if (!data.sync.paths.length) paths.textContent = "未配置同步路径";
      if (data.scheduler.last_result) show(data.scheduler.last_result);
    }

    async function loadStatus() {
      const data = await api("/api/status");
      render(data);
    }

    async function run(path) {
      setBusy(true);
      try {
        const data = await api(path, { method: "POST" });
        show(data);
        await loadStatus();
      } catch (error) {
        badge($("taskState"), "出错", "red");
        show(error);
      } finally {
        setBusy(false);
      }
    }

    $("sync").onclick = () => run("/sync");
    $("dry").onclick = () => run("/sync?dry_run=true");
    $("refresh").onclick = () => run("/api/media/refresh");
    $("reload").onclick = loadStatus;
    loadStatus().catch(show);
    setInterval(loadStatus, 10000);
  </script>
</body>
</html>
"""
