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
      --panel: rgba(255,255,255,.88);
      --line: #d9dee7;
      --text: #374151;
      --muted: #7a8190;
      --purple: #8b5cf6;
      --blue: #0ea5e9;
      --green: #52c41a;
      --orange: #f59e0b;
      --red: #ff4d4f;
      --info: #e6f7ff;
      --shadow: 0 8px 22px rgba(15, 23, 42, .08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background: linear-gradient(115deg, #e7f7ff, #fff1f7 44%, #fff 76%);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
    }
    header {
      height: 38px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 14px;
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,.65);
      font-weight: 800;
      color: #5f6675;
    }
    .logo { color: var(--purple); }
    main { padding: 12px 12px 72px; }
    .layout {
      display: grid;
      grid-template-columns: minmax(360px, 1fr) minmax(420px, 1fr);
      gap: 24px;
      align-items: start;
    }
    .stack { display: grid; gap: 16px; }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 14px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .card-title {
      min-height: 34px;
      display: flex;
      align-items: center;
      padding: 0 18px;
      background: linear-gradient(110deg, rgba(219,242,255,.82), rgba(255,239,246,.75));
      font-weight: 800;
      color: #536071;
    }
    .card-body { padding: 14px 18px; }
    .row {
      min-height: 39px;
      display: grid;
      grid-template-columns: 24px 1fr auto;
      gap: 10px;
      align-items: center;
      border-bottom: 1px solid rgba(217,222,231,.72);
    }
    .row:last-child { border-bottom: 0; }
    .icon { color: var(--purple); font-weight: 900; text-align: center; }
    .label { color: #626b7c; }
    .hint { color: var(--muted); font-size: 13px; line-height: 1.55; }
    .badge {
      min-width: 54px;
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
      max-width: 260px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .green { background: #f0fdf4; color: var(--green); }
    .orange { background: #fffbeb; color: var(--orange); }
    .gray { background: #f3f4f6; color: #8a8f99; }
    .red { background: #fff1f2; color: var(--red); }
    .path-list, .library-list { display: grid; gap: 10px; }
    .path-pair, .library-item {
      display: grid;
      gap: 10px;
      align-items: center;
      min-height: 62px;
      padding: 10px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,.68);
    }
    .path-pair { grid-template-columns: 1fr 54px 1fr; }
    .library-item { grid-template-columns: 24px 120px 1fr; }
    .path-box {
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 8px;
      align-items: center;
      min-width: 0;
    }
    code {
      color: #5f6675;
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      word-break: break-all;
    }
    .notice {
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 8px;
      align-items: start;
      padding: 12px 16px;
      border-radius: 7px;
      background: var(--info);
      color: #1677ff;
      margin-bottom: 14px;
      line-height: 1.6;
    }
    .control-grid {
      display: grid;
      grid-template-columns: minmax(160px, 1fr) minmax(220px, 1fr);
      gap: 12px;
      margin-bottom: 14px;
    }
    .field {
      min-height: 42px;
      display: grid;
      gap: 5px;
    }
    .field label {
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }
    select {
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 0 10px;
      background: #fff;
      color: var(--text);
      font-weight: 700;
    }
    .checkline {
      min-height: 38px;
      display: flex;
      align-items: center;
      gap: 9px;
      color: #626b7c;
      font-weight: 700;
    }
    input[type="checkbox"] { width: 18px; height: 18px; accent-color: var(--purple); }
    .library-tools {
      display: flex;
      gap: 10px;
      margin: 6px 0 10px;
    }
    .library-tools button {
      min-height: 30px;
      padding: 0 10px;
      font-size: 13px;
    }
    .actions {
      display: grid;
      grid-template-columns: repeat(4, minmax(110px, 1fr));
      gap: 10px;
      margin: 14px 0;
    }
    button {
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: #6d28d9;
      font-weight: 800;
      cursor: pointer;
    }
    button.primary { color: #fff; background: var(--orange); border-color: var(--orange); }
    button:disabled { opacity: .58; cursor: wait; }
    .result {
      min-height: 190px;
      max-height: 360px;
      overflow: auto;
      padding: 12px;
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
      padding: 8px 14px;
      background: rgba(255,255,255,.93);
      border-top: 1px solid var(--line);
      box-shadow: 0 -8px 20px rgba(15,23,42,.08);
      color: var(--muted);
      font-size: 13px;
    }
    @media (max-width: 920px) {
      .layout { grid-template-columns: 1fr; }
      .actions, .control-grid { grid-template-columns: 1fr; }
      .path-pair, .library-item { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header><span class="logo">STRM</span><span>115网盘STRM助手</span></header>
  <main>
    <section class="layout">
      <div class="stack">
        <article class="card">
          <div class="card-title">系统状态</div>
          <div class="card-body">
            <div class="row"><span class="icon">P</span><span class="label">服务状态</span><span class="badge green">已启用</span></div>
            <div class="row"><span class="icon">C</span><span class="label">115 Cookie</span><span id="cookieState" class="badge gray">读取中</span></div>
            <div class="row"><span class="icon">T</span><span class="label">同步任务</span><span id="taskState" class="badge orange">读取中</span></div>
          </div>
        </article>

        <article class="card">
          <div class="card-title">同步配置</div>
          <div class="card-body">
            <div class="row"><span class="icon">F</span><span class="label">全量同步 Cron</span><span id="fullCron" class="badge gray">-</span></div>
            <div class="row"><span class="icon">I</span><span class="label">增量同步 Cron</span><span id="incrementCron" class="badge gray">-</span></div>
            <div class="row"><span class="icon">M</span><span class="label">媒体库刷新</span><span id="mediaRefreshState" class="badge gray">读取中</span></div>
            <div class="row"><span class="icon">U</span><span class="label">STRM 访问地址</span><span id="publicUrl" class="badge gray">-</span></div>
            <div class="row"><span class="icon">L</span><span class="label">单次扫描上限</span><span id="scanLimit" class="badge gray">-</span></div>
            <div class="row"><span class="icon">B</span><span class="label">批次休眠</span><span id="batchSleep" class="badge gray">-</span></div>
          </div>
        </article>

        <article class="card">
          <div class="card-title">路径配置</div>
          <div class="card-body">
            <div id="paths" class="path-list"></div>
          </div>
        </article>
      </div>

      <div class="stack">
        <article class="card">
          <div class="card-title">手动控制</div>
          <div class="card-body">
            <div class="notice">
              <strong>i</strong>
              <div>
                先选择媒体库，再选择增量或全量。增量只补缺失 STRM；全量会在受控上限内重写所选媒体库的 STRM。
              </div>
            </div>
            <div class="control-grid">
              <div class="field">
                <label for="syncMode">同步模式</label>
                <select id="syncMode">
                  <option value="increment">增量同步：只补缺失 STRM</option>
                  <option value="full">全量同步：重新生成 STRM</option>
                </select>
              </div>
              <label class="checkline">
                <input id="refreshAfterSync" type="checkbox" checked>
                同步后刷新媒体库
              </label>
            </div>

            <div class="field">
              <label>选择媒体库</label>
              <div class="library-tools">
                <button id="selectAll" type="button">全选</button>
                <button id="selectNone" type="button">全不选</button>
              </div>
              <div id="libraries" class="library-list"></div>
            </div>

            <div class="actions">
              <button id="reload">刷新状态</button>
              <button id="dry">干跑预览</button>
              <button id="refresh">仅刷新媒体库</button>
              <button class="primary" id="sync">开始同步</button>
            </div>
            <div class="result" id="result">等待操作...</div>
          </div>
        </article>
      </div>
    </section>
  </main>
  <footer class="dock">
    <span>p115-strm-lite</span>
    <span>页面每 10 秒自动刷新状态</span>
  </footer>

  <script>
    const $ = (id) => document.getElementById(id);
    const buttons = [...document.querySelectorAll("button")];

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

    function checkedLibraryIndexes() {
      return [...document.querySelectorAll(".library-check:checked")].map((input) => input.value);
    }

    function syncQuery(dryRun) {
      const params = new URLSearchParams({
        mode: $("syncMode").value,
        dry_run: dryRun ? "true" : "false",
        refresh_media: $("refreshAfterSync").checked ? "true" : "false",
      });
      for (const index of checkedLibraryIndexes()) params.append("path_index", index);
      return "/sync?" + params.toString();
    }

    function renderLibraries(pathsData) {
      const selectedBefore = new Set(checkedLibraryIndexes());
      const libraries = $("libraries");
      libraries.innerHTML = "";
      for (const item of pathsData) {
        const checked = selectedBefore.size === 0 || selectedBefore.has(String(item.index));
        const label = document.createElement("label");
        label.className = "library-item";
        label.innerHTML = `
          <input class="library-check" type="checkbox" value="${item.index}" ${checked ? "checked" : ""}>
          <strong>${item.label}</strong>
          <span class="hint"><code>${item.pan_path}</code> -> <code>${item.local_path}</code></span>
        `;
        libraries.appendChild(label);
      }
      if (!pathsData.length) libraries.textContent = "未配置媒体库路径";
    }

    function render(data) {
      badge($("cookieState"), data.auth.has_p115_cookies ? "已连接" : "未配置", data.auth.has_p115_cookies ? "green" : "red");
      badge($("taskState"), data.scheduler.running ? "运行中" : "空闲", data.scheduler.running ? "orange" : "green");
      badge($("mediaRefreshState"), data.media_server.enabled ? "已启用" : "已禁用", data.media_server.enabled ? "green" : "gray");
      $("refreshAfterSync").disabled = !data.media_server.enabled;
      if (!data.media_server.enabled) $("refreshAfterSync").checked = false;
      $("fullCron").textContent = data.sync.full_cron || "-";
      $("incrementCron").textContent = data.sync.increment_cron || "-";
      $("publicUrl").textContent = data.server.public_url || "-";
      $("scanLimit").textContent = data.sync.max_files_per_run > 0 ? data.sync.max_files_per_run : "不限";
      $("batchSleep").textContent = `${data.sync.batch_size} / ${data.sync.batch_sleep_seconds}s`;

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
      renderLibraries(data.sync.paths);
      if (data.scheduler.last_result) show(data.scheduler.last_result);
    }

    async function loadStatus() {
      const data = await api("/api/status");
      render(data);
      return data;
    }

    async function run(path) {
      if (path.startsWith("/sync") && checkedLibraryIndexes().length === 0) {
        show({ error: "请至少选择一个媒体库" });
        return;
      }
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

    $("sync").onclick = () => run(syncQuery(false));
    $("dry").onclick = () => run(syncQuery(true));
    $("refresh").onclick = () => run("/api/media/refresh");
    $("reload").onclick = () => loadStatus().then(show).catch(show);
    $("selectAll").onclick = () => document.querySelectorAll(".library-check").forEach((input) => input.checked = true);
    $("selectNone").onclick = () => document.querySelectorAll(".library-check").forEach((input) => input.checked = false);
    loadStatus().catch(show);
    setInterval(() => loadStatus().catch(show), 10000);
  </script>
</body>
</html>
"""
