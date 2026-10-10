# CPPAI Agents Plugins

Plugins and agent skills by [CPPAI](https://cpp.ai.vn) for Claude Code and other coding agents.

## Install the marketplace

This repository is a plugin marketplace named `cppai` for Claude Code, Codex, GitHub Copilot CLI, Cursor and oh-my-pi. Add it, then install the plugins you need:

| Agent | Add the marketplace | Install a plugin |
|---|---|---|
| Claude Code | `/plugin marketplace add cppai-vn/agents-plugins` | `/plugin install ezyplatform@cppai` |
| Codex | `codex plugin marketplace add cppai-vn/agents-plugins` | `codex plugin add ezyplatform@cppai` |
| Copilot CLI | `copilot plugin marketplace add cppai-vn/agents-plugins` | `copilot plugin install ezyplatform@cppai` |
| Cursor | Customize → From GitHub Repository → `https://github.com/cppai-vn/agents-plugins` | Install from the list |
| oh-my-pi | `omp plugin marketplace add cppai-vn/agents-plugins` | `omp plugin install ezyplatform@cppai` |

Update commands and per-agent notes are in each plugin's README.

## Plugins

| Plugin | Description |
|---|---|
| [`ezyplatform`](ezyplatform) | Manage EzyPlatform / EzyArticle sites from a local project: init, sync, author, media, i18n, publish with backup and rollback, verify. |

## Other agents

Agents without a plugin system can still use the skills: each plugin keeps them in `<name>/skills/` using the open `SKILL.md` format. Copy those folders into your project's `.claude/skills/` or `.agents/skills/` — see each plugin's README.

## Repository layout

```
.claude-plugin/marketplace.json   # marketplace "cppai": lists every plugin (Claude Code, Codex, Copilot CLI, oh-my-pi)
.cursor-plugin/marketplace.json   # the same list for Cursor, which only reads this path
<name>/.claude-plugin/plugin.json   # plugin manifest; the only place "version" lives
<name>/.cursor-plugin/plugin.json   # same manifest for Cursor, without "version"
<name>/skills/<skill>/SKILL.md
<name>/README.md
```

Adding a plugin: create `<name>/` with both manifests, skills and `CHANGELOG.md`, add an entry to both marketplace files (without `version`), and run `claude plugin validate . --strict`. CI fails when the two marketplace files list different plugins or a Cursor manifest is missing.

Releasing: users only receive an update when `version` in `<name>/.claude-plugin/plugin.json` changes, and installed plugins run from a per-version cache. Release with one command (dry run without `--yes`):

```bash
python3 scripts/release_plugin.py <name> patch|minor|major -n "change" -m "fix(<name>): summary" --push --install --yes
```

It bumps the version, adds the `CHANGELOG.md` entry, validates, commits, pushes and runs `claude plugin marketplace update` + `claude plugin update` locally. CI checks the version and CHANGELOG on GitHub.

## License

MIT — see [LICENSE](LICENSE), unless a plugin states otherwise.
