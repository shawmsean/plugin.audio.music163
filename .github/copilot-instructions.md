# Copilot / AI Agent 指南（针对 plugin.audio.music163）

目的：帮助 AI 代码代理快速上手此 Kodi 插件代码库，聚焦可执行信息与项目特性。

- **整体架构（大局观）**：`addon.py` 是插件入口（xbmc.python pluginsource），通过 `xbmcswift2.Plugin` 注册路由并负责 UI/播放逻辑；`addon.py` 大量调用 `api.py` 中的 `NetEase` 客户端以执行网易云接口请求；`encrypt.py` 提供与网抑云 API 兼容的加密（`encrypted_request`、`encrypted_id`）。`TuneHubMusiAPI.py` 当前为空。

- **运行时与调试**：
  - 插件设计在 Kodi 环境下运行，依赖 Kodi 提供的模块：`xbmc`、`xbmcaddon`、`xbmcplugin`、`xbmcvfs`，以及第三方 `xbmcswift2`。
  - 插件配置与运行时参数经由 `xbmcplugin.getSetting(...)` 和 `xbmcaddon.Addon().getAddonInfo('profile')` 传入。
  - 在本地（非 Kodi）调试 `api.py` 或部分逻辑时，请 mock/替换 `xbmc*` 与 `xbmcswift2` 的最小接口，并确保 `PROFILE` 目录存在以产生 `cookie.txt`。

- **关键文件（优先阅读）**：
  - `addon.py`：路由定义、播放控制、持久化存储包装（见 `safe_get_storage()`）以及 `get_songs()` 的响应规范化。
  - `api.py`：`NetEase` 类封装所有网络请求、cookie 管理、代理开关与加密集成点（调用 `encrypted_request()`）。
  - `encrypt.py`：实现 Netease 所需的请求/ID 加密函数（可直接复用）。
  - `addon.xml`：列出运行时依赖（用于打包/安装时参考）。
  - `README.md`：变更日志示例（如新增 `play_recommend_songs()`、`play_playlist_songs()`），可帮助理解近期功能目的。

- **项目约定与模式**：
  - 路由由 `@plugin.route('/path/')` 装饰器定义；在 `addon.py` 搜索该装饰器可发现所有可调用路径。
  - 持久化使用 `plugin.get_storage(name)`，但代码提供 `safe_get_storage(name)` 以在 IO/权限错误时返回带默认结构的回退字典（请在新增存储时沿用此函数）。
  - 所有对网易云的请求通过 `NetEase.request()` 统一：会从 cookie 注入 `csrf_token`、用 `encrypted_request()` 构造请求体，并在登录后调用 `self.session.cookies.save()` 保存 cookie。
  - cookie 存放路径为 `PROFILE/cookie.txt`（由 `xbmcaddon.Addon().getAddonInfo('profile')` 决定）；不要在代码中硬编码其他路径。

- **外部依赖（见 `addon.xml`）**：`xbmc.python`、`script.module.xbmcswift2`、`requests`、`beautifulsoup4`、`future`、`qrcode`、`html5lib`。

- **常见易错点（务必注意）**：
  - 代码普遍假定在 Kodi 环境中运行；脱离 Kodi 时要提供最小 mock。示例：`xbmcvfs.translatePath`、`xbmcplugin.getSetting()`。
  - `get_songs()` 对不同 API 返回结构做了大量兼容与规范化；新增调用方应遵循其输出字段（例如 `id`、`artist`、`picUrl`、`privilege`），以避免 KeyError/None。
  - 存储可能因权限或磁盘问题失败，使用 `safe_get_storage()` 并保持默认键（如 `liked_songs` 的 `pid`/`ids`，`account` 的 `uid`/`logined` 等）。

- **AI 代理上手建议（优先执行）**：
  1. 通读 `addon.py` 以掌握路由与播放逻辑（重点：`get_songs()`、播放相关的 helper 函数）。
  2. 阅读 `api.py`，理解如何构造请求、如何使用 `encrypt.py`，以及 cookie/代理的处理逻辑。
  3. 若需新增 API，优先在 `api.py` 增加方法并在 `addon.py` 中找到对应路由或调用点进行接入；保持 cookie 与 `csrf_token` 的注入方式一致。

- **编辑与本地测试建议**：
  - 对会在 Kodi 中运行的代码做小而可回退的改动；将可测试逻辑抽离为小函数，方便在无 Kodi 环境下单元测试。
  - 本地调试网络时，可用临时目录替换 `xbmcaddon.Addon().getAddonInfo('profile')`，以确保 `COOKIE_PATH` 可写：

```powershell
# 在调试脚本中示例替换（PowerShell）
# 设置环境变量或在测试入口处 monkeypatch xbmcaddon.Addon().getAddonInfo('profile')
```

- **如果需要我可以继续做的事情**：
  - 为 `TuneHubMusiAPI.py` 搭建本地测试骨架（含对 `xbmc*` 的最小 mock 和示例调用）。
  - 为 `api.py` 添加更完整的本地单元测试示例并生成 `requirements.txt`。

如需我马上改写或补充上面的任一部分，请告诉我具体优先项。
