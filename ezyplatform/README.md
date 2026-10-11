# EzyPlatform plugin

Agent skills that let you manage an [EzyPlatform](https://ezyplatform.com) / EzyArticle site by talking to your coding agent ("vibe coding" for EzyPlatform): set up a project, pull content, redesign pages, manage media and translations, publish safely with backup and rollback, and verify the live site.

Bộ skill giúp quản trị site EzyPlatform / EzyArticle bằng cách trò chuyện với AI agent: khởi tạo dự án, kéo nội dung, thiết kế lại trang, quản lý media và bản dịch, publish an toàn (có sao lưu và khôi phục), kiểm tra site thật. [Hướng dẫn tiếng Việt ↓](#tiếng-việt)

| Skill | What it does |
|---|---|
| `ezy-guide` | Start here: picks the right skill and workflow, safety rules, verified platform gotchas |
| `ezy-init` | Scaffolds a project like the EzyArticle VS Code "Create Project" command and walks you through getting the admin access token |
| `ezy-sync` | Compares local files with the server, pulls pages/fragments (incl. translations), `pull-all` |
| `ezy-author` | Writes and redesigns pages, fragments and themes (HTML/Thymeleaf/CSS/JS), light/dark, multilingual |
| `ezy-media` | Uploads/replaces media library files, visibility, cache-busted URLs |
| `ezy-i18n` | Diffs and pushes UI message translations (only changed keys) |
| `ezy-publish` | Dry-run plan → backup → per-language publish → verify → one-command rollback; remove to Trash with undo |
| `ezy-mail` | EzyMail delivery health, mail templates, EzySupport Contact Us settings and end-to-end form test |
| `ezy-verify` | Local preview with fragments inlined, live checks (status, unrendered markers, expected text) |

All writes to your site run as a dry run first and need your explicit approval. The admin token stays in your local `environment.json` and is never printed.

## Requirements

- An EzyPlatform admin account and its access token
- Python 3.9+ (scripts use only the standard library)
- Optional: the [EzyArticle VS Code extension](https://marketplace.visualstudio.com/items?itemName=youngmonkeys.ezyarticle) and Node.js (used to pick up its latest agent instructions)

## Install

The same repository is a plugin marketplace named `cppai` for every agent below. Install it once per agent you use; each agent keeps its own copy, so updates are per agent too. Start a new session after installing or updating — skills load at session start.

| Agent | Install | Update |
|---|---|---|
| Claude Code | `/plugin marketplace add cppai-vn/agents-plugins`<br>`/plugin install ezyplatform@cppai` | `/plugin marketplace update cppai`<br>`/plugin update ezyplatform@cppai` |
| Codex CLI / app | `codex plugin marketplace add cppai-vn/agents-plugins`<br>`codex plugin add ezyplatform@cppai` (or `/plugins` in the TUI) | `codex plugin marketplace upgrade cppai` |
| GitHub Copilot CLI | `copilot plugin marketplace add cppai-vn/agents-plugins`<br>`copilot plugin install ezyplatform@cppai` | `copilot plugin marketplace update cppai`<br>`copilot plugin update ezyplatform` |
| Cursor | **Customize** → **From GitHub Repository** → `https://github.com/cppai-vn/agents-plugins` → install **ezyplatform** (project or user scope). Teams: add the repo under Dashboard → Plugins & MCPs → Team Marketplaces | Reinstall, or enable Auto Refresh on a team marketplace |
| oh-my-pi (`omp`) | `omp plugin marketplace add cppai-vn/agents-plugins`<br>`omp plugin install ezyplatform@cppai` (or `/marketplace` in the TUI) | `omp plugin marketplace update cppai`<br>`omp plugin upgrade ezyplatform@cppai` |

Skills appear namespaced in agents that support it (e.g. `ezyplatform:ezy-guide`). Only Claude Code fills in `${CLAUDE_SKILL_DIR}` in the skill instructions; the other agents follow the note at the top of each `SKILL.md` and use the folder that contains it.

Install in only one way per agent: the plugin, or a copied `skills/` folder (below), not both — otherwise the agent sees every skill twice.

### Agents without plugins, or a pinned copy

Agents that read skill folders but not plugins (OpenCode, Factory Droid, Kiro, Roo, Windsurf, …) — copy the `skills/` folder into your site project:

```bash
git clone https://github.com/cppai-vn/agents-plugins.git agents-plugins
mkdir -p .claude/skills && cp -R agents-plugins/ezyplatform/skills/ezy-* .claude/skills/      # Claude Code
mkdir -p .agents/skills && cp -R agents-plugins/ezyplatform/skills/ezy-* .agents/skills/      # agents reading .agents/skills
```

Keep `ezy-shared` next to the other skills; every script imports it.

## Quick start

1. Open an empty folder for your site in your agent and say: *"Initialize an EzyPlatform project for https://admin.example.com"* — `ezy-init` creates `environment.json`, `AGENTS.md`, `README.md`, starter folders and `.gitignore`.
2. Get your token: open `https://admin.example.com/admins/me`, reveal **Access Token** (confirm with your password) and paste it into `environment.json` → the `"default": true` entry → `admin_access_token`. Do not paste it into the chat.
3. Say *"Check the EzyPlatform setup"* — the agent validates the connection and shows your role and site URL.
4. Say *"Pull the site content"*, then describe the change you want, e.g. *"Redesign the home page in a modern dark style, keep Vietnamese and English in sync"*. The agent previews, asks before publishing, publishes with a backup and verifies the live site.

## Safety

- `environment.json` is git-ignored and created with `chmod 600`; the token carries the full rights of its admin account — prefer a dedicated admin with content/media rights only, and regenerate the token if it leaks.
- Publishing only updates existing posts; every publish stores a backup in `.artifacts/backups/` and prints a rollback command.
- Never publish personal data from source documents (ID numbers, registration scans).

## Contributing

The skills improve from real use: after each operation the agent suggests concrete skill changes. Open an issue or pull request with the suggestion and its evidence. Verified platform behaviour lives in `skills/ezy-guide/references/platform-gotchas.md` (inside `ezyplatform/`).

Developed and tested on [cpp.ai.vn](https://cpp.ai.vn).

## License

MIT — see [LICENSE](../LICENSE). The starter templates in `skills/ezy-init/templates/` come from the EzyArticle VS Code extension by YoungMonkeys (MIT); see `skills/ezy-init/templates/NOTICE.md`.

---

## Tiếng Việt

**Cài đặt:** repo này là marketplace `cppai` dùng chung cho các agent có cơ chế plugin. Cài riêng cho từng agent bạn dùng, sau khi cài hoặc cập nhật thì mở session mới.

| Agent | Cài | Cập nhật |
|---|---|---|
| Claude Code | `/plugin marketplace add cppai-vn/agents-plugins`<br>`/plugin install ezyplatform@cppai` | `/plugin marketplace update cppai`<br>`/plugin update ezyplatform@cppai` |
| Codex CLI / app | `codex plugin marketplace add cppai-vn/agents-plugins`<br>`codex plugin add ezyplatform@cppai` (hoặc `/plugins` trong TUI) | `codex plugin marketplace upgrade cppai` |
| GitHub Copilot CLI | `copilot plugin marketplace add cppai-vn/agents-plugins`<br>`copilot plugin install ezyplatform@cppai` | `copilot plugin marketplace update cppai`<br>`copilot plugin update ezyplatform` |
| Cursor | **Customize** → **From GitHub Repository** → `https://github.com/cppai-vn/agents-plugins` → cài **ezyplatform**. Team: thêm repo ở Dashboard → Plugins & MCPs → Team Marketplaces | Cài lại, hoặc bật Auto Refresh cho team marketplace |
| oh-my-pi (`omp`) | `omp plugin marketplace add cppai-vn/agents-plugins`<br>`omp plugin install ezyplatform@cppai` (hoặc `/marketplace` trong TUI) | `omp plugin marketplace update cppai`<br>`omp plugin upgrade ezyplatform@cppai` |

Mỗi agent chỉ cài một kiểu: hoặc plugin, hoặc chép thư mục skill, không cả hai (nếu không skill sẽ hiện hai lần).

Agent không có plugin (OpenCode, Droid, Kiro, Roo, Windsurf…): chép thư mục `skills/ezy-*` vào `.claude/skills/` hoặc `.agents/skills/` của dự án site, nhớ giữ cả `ezy-shared`.

**Bắt đầu:**

1. Mở một thư mục trống cho site và nói: *"Khởi tạo dự án EzyPlatform cho https://admin.example.com"*.
2. Lấy token: vào `https://admin.example.com/admins/me`, bấm hiện **Access Token** (nhập mật khẩu), rồi tự dán vào `environment.json` → mục `"default": true` → `admin_access_token`. Không dán token vào khung chat.
3. Nói *"Kiểm tra cấu hình EzyPlatform"* để agent xác nhận kết nối.
4. Nói *"Kéo nội dung site về"*, rồi mô tả thay đổi bạn muốn. Agent sẽ xem trước, hỏi trước khi publish, sao lưu và kiểm tra site thật sau khi publish.

**An toàn:** mọi thao tác ghi lên site đều chạy thử trước và cần bạn duyệt; token chỉ nằm trong máy bạn, không bị in ra.
