---
name: ezy-publish
description: Publish local EzyArticle pages and page fragments to the live EzyPlatform site (local → server) with a dry-run plan, automatic backup, per-language updates, post-write verification and one-command rollback. Use when the user asks to deploy, publish, push or go live with site changes, or to roll back a publish.
---

# ezy-publish

> Paths: `<skills>` is the folder that holds the ezy-* skills (the parent of this skill's base directory — the plugin's `skills/`, `.claude/skills` or `.agents/skills`). Run commands from the site project root (the folder with `environment.json`).

Local → server. This changes what visitors see. Read `ezy-guide` (safety rules, gotchas 2–6) first.

## Workflow

1. **Drift check** — `ezy-sync status` for the targets. If the server differs from what you started from, stop and tell the human (someone else edited it).
2. **Preview** — `ezy-verify preview` for affected pages; fix layout issues before publishing.
3. **Plan (dry run)**
   ```bash
   python3 <skills>/ezy-publish/scripts/ezy_publish.py plan fragment:cppai/theme page:home
   ```
   Shows per target and language which fields change. Fragments are ordered before pages automatically.
4. **Ask the human** — show the plan and get explicit approval for this publish.
5. **Apply**
   ```bash
   python3 <skills>/ezy-publish/scripts/ezy_publish.py apply fragment:cppai/theme page:home --yes
   ```
   Backs up each live post to `.artifacts/backups/<timestamp>/`, PUTs only changed fields, re-reads and verifies, prints the rollback command. Stops at the first failure.
6. **Verify live** — `ezy-verify live` (both languages, expected texts), plus a visual check if layout changed.
7. **Rollback if needed** (also needs approval)
   ```bash
   python3 <skills>/ezy-publish/scripts/ezy_publish.py restore .artifacts/backups/<timestamp> --yes
   ```

## Rules

- Only existing server posts are updated. A brand-new page/fragment must be created once with the VS Code extension (`EzyArticle: Publish Content To Server`), then managed here. If this keeps coming up, propose adding create support.
- Live `status`, `slug`, `postType`, `contentType` and menu link are preserved; the script warns when `meta.json` status disagrees.
- Media referenced by the new markup must already exist (`ezy-media status`); UI strings must already be pushed (`ezy-i18n`) before markup that uses new keys goes live.
- Publish order for shared changes: theme/CSS fragments → header/footer → pages.
- Do not commit or push git as part of publishing unless the human asks.

## Finish

Report what went live (targets × languages), the backup path, verification results, then run the improvement check (`references/skill-improvement.md` of `ezy-guide`).
