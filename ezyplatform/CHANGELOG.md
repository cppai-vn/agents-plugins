# Changelog — ezyplatform plugin

Users receive an update only when `version` in `.claude-plugin/plugin.json` changes; bump it for every release and record the change here.

## 0.2.0 — 2026-10-10

- SKILL.md files reference bundled scripts through `${CLAUDE_SKILL_DIR}`, so the same files work as a plugin and as a copied `.claude/skills` / `.agents/skills` folder.
- Version is declared only in `plugin.json` (removed from the marketplace entry).
- CI validates the marketplace and plugin manifests and the Python scripts on every push and pull request.

## 0.1.0 — 2026-10-10

- First release: `ezy-guide`, `ezy-init`, `ezy-sync`, `ezy-author`, `ezy-media`, `ezy-i18n`, `ezy-publish`, `ezy-verify` and the shared `ezy-shared` library.
