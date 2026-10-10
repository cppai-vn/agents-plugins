# CPPAI Agents Plugins

Plugins and agent skills by [CPPAI](https://cpp.ai.vn) for Claude Code and other coding agents.

## Install the marketplace (Claude Code)

```
/plugin marketplace add cppai-vn/agents-plugins
```

Then install the plugins you need, e.g. `/plugin install ezyplatform@cppai`. Update with `/plugin marketplace update cppai`.

## Plugins

| Plugin | Description |
|---|---|
| [`ezyplatform`](ezyplatform) | Manage EzyPlatform / EzyArticle sites from a local project: init, sync, author, media, i18n, publish with backup and rollback, verify. |

## Other agents

Each plugin keeps its skills in `<name>/skills/` using the open `SKILL.md` format. Copy those folders into your project's `.claude/skills/` or `.agents/skills/` — see each plugin's README.

## Repository layout

```
.claude-plugin/marketplace.json   # marketplace "cppai": lists every plugin
<name>/.claude-plugin/plugin.json
<name>/skills/<skill>/SKILL.md
<name>/README.md
```

Adding a plugin: create `<name>/` with its manifest, skills and `CHANGELOG.md`, add an entry to `marketplace.json` (without `version`), and run `claude plugin validate . --strict`.

Releasing: users only receive an update when `version` in `<name>/.claude-plugin/plugin.json` changes, and installed plugins run from a per-version cache. Release with one command (dry run without `--yes`):

```bash
python3 scripts/release_plugin.py <name> patch|minor|major -n "change" -m "fix(<name>): summary" --push --install --yes
```

It bumps the version, adds the `CHANGELOG.md` entry, validates, commits, pushes and runs `claude plugin marketplace update` + `claude plugin update` locally. CI checks the version and CHANGELOG on GitHub.

## License

MIT — see [LICENSE](LICENSE), unless a plugin states otherwise.
