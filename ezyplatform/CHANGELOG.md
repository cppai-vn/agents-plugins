# Changelog — ezyplatform plugin

Users receive an update only when `version` in `.claude-plugin/plugin.json` changes; bump it for every release and record the change here.

## 0.3.0 — 2026-10-10

- ezy-sync: local-only draft pages no longer abort pull-all or count as drift
- ezy-sync: discover-pages finds and pulls pages linked from local HTML
- ezy-sync: pull-all --skip-placeholders leaves out empty theme fragments

## 0.2.3 — 2026-10-10

- Add scripts/release_plugin.py: one-step version bump, CHANGELOG entry, strict validation, commit, push and local plugin refresh for maintainers
- ezy-guide improvement loop points maintainers to the release script

## 0.2.2 — 2026-10-10

- `ezy-guide`: correct the update note — installed plugins run from a per-version cache, also for local-folder marketplaces, so a version bump plus `plugin update` is required before a new session sees changes.

## 0.2.1 — 2026-10-10

- `ezy-guide`: maintainers are told that edited skills load only in a new session, and the release steps (version bump, CHANGELOG, marketplace update) are part of the improvement loop.

## 0.2.0 — 2026-10-10

- SKILL.md files reference bundled scripts through `${CLAUDE_SKILL_DIR}`, so the same files work as a plugin and as a copied `.claude/skills` / `.agents/skills` folder.
- Version is declared only in `plugin.json` (removed from the marketplace entry).
- CI validates the marketplace and plugin manifests and the Python scripts on every push and pull request.

## 0.1.0 — 2026-10-10

- First release: `ezy-guide`, `ezy-init`, `ezy-sync`, `ezy-author`, `ezy-media`, `ezy-i18n`, `ezy-publish`, `ezy-verify` and the shared `ezy-shared` library.
