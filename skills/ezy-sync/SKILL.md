---
name: ezy-sync
description: Compare and pull EzyPlatform pages and page fragments from the live server into the local EzyArticle project (server → local, read-only for the site). Use before editing a site, when the user asks whether local files are up to date, after someone edited content in the admin UI, or to fetch a translated (`<lang>`) version of a page or fragment.
---

# ezy-sync

> Paths: `<skills>` is the folder that holds the ezy-* skills (the parent of this skill's base directory — the plugin's `skills/`, `.claude/skills` or `.agents/skills`). Run commands from the site project root (the folder with `environment.json`).

Server → local. Never writes to the site. Read `ezy-guide` first if you have not.

## Check drift

```bash
python3 <skills>/ezy-sync/scripts/ezy_sync.py status            # all local targets
python3 <skills>/ezy-sync/scripts/ezy_sync.py status page:home fragment:cppai/header
```

- Compares `content`, `head`, `foot`, `title`, `summary` for the default language and every language that has localized files locally.
- Exit code 1 when anything differs — treat that as "someone changed the site" and pull before editing.
- Localized `summary` is skipped on purpose (the server keeps one summary; gotcha 5).

## Pull

```bash
python3 <skills>/ezy-sync/scripts/ezy_sync.py pull fragment:cppai/header --lang en          # dry run
python3 <skills>/ezy-sync/scripts/ezy_sync.py pull fragment:cppai/header --lang en --write
```

- Dry run by default; `--write` overwrites `content/head/foot[.<lang>].html`.
- `meta.json` / `meta.<lang>.json` is **created when missing** (extension format: title, summary, slug, pageType, contentType, status, priority, publishedAt, terms, metadata; localized meta = title only, skipped when the server has no translation). An existing meta is never rewritten (local-only fields survive); differing titles are reported for a manual edit.
- Pulling into a folder that does not exist yet creates it, so `pull` also brings a new page or fragment under local management.
- Localized fragments are read via `/posts/{id}?i18n_lang=` because the fragment endpoint ignores the language (gotcha 2).
- If local files have uncommitted edits, show `git diff` to the human before `--write`.

## Pull everything

```bash
python3 <skills>/ezy-sync/scripts/ezy_sync.py pull-all --langs en                 # dry run: every fragment + local pages
python3 <skills>/ezy-sync/scripts/ezy_sync.py pull-all --only cppai --langs en --write
```

- Covers every fragment the server lists (`/pages/fragments`) plus pages already present locally — there is no page-listing API, so pull a new page once with `pull page:<slug> --write`.
- `--only <page_name ...>` limits fragments to some groups (a theme may ship dozens of fragments you never edit).
- Run `git status` first; with `--write` it overwrites local regions that differ.
- The dry-run count can be higher than the real write: localized regions are compared against default files that do not exist yet.

## Not covered (use the VS Code extension for now)

Posts, terms, mail/content templates, media download. If you need one of these repeatedly, propose a script extension via the improvement check.

## Finish

Report which targets differed and what was pulled, then run the improvement check (`references/skill-improvement.md` of `ezy-guide`).
