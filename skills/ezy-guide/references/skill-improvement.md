# Skill improvement loop

This project manages a real site **and** grows the `ezy-*` skill set. Every
operation on a site is also a test of the skills.

## When

At the end of any operation that touched an EzyPlatform site or its local files
(sync, author, media, i18n, publish, verify, debugging).

## What to look for

- A step done by hand that a script could do (repeated curl/python, manual diffing).
- A server behaviour that surprised you → candidate entry for `platform-gotchas.md`.
- An instruction that was wrong, stale, missing or ambiguous.
- A script error, confusing output, or missing guard (dry run, backup, verify).
- A recurring task with no owning skill → candidate new `ezy-<name>` skill.
- A user correction about design, copy or process that should become a rule.

## How to propose

Do **not** edit skills silently. End the report to the human with:

```
Skill suggestions (need approval):
1. [ezy-<skill>] <change> — why: <evidence from this run> — effort: S/M/L
2. [new: ezy-<name>] <purpose> — why: <evidence>
```

Say "No skill suggestions" when nothing qualifies, so the check is visible.

## Where the change goes

- Skills installed as the `ezyplatform-skills` plugin are a read-only cache: never edit them in place. Open an issue or pull request at the skills repository (see the plugin's README), including the evidence.
- Skills vendored in the project (`.claude/skills`, `.agents/skills`) or a local clone of the repository may be edited after approval; upstream the change afterwards so every EzyPlatform user gets it.

## After approval

1. Make the smallest change that fixes the observed friction (frontmatter, SKILL.md step, reference, or script).
2. Run the touched script in its read-only / dry-run mode against the live site.
3. Record new verified platform facts in `platform-gotchas.md` with an evidence line.
4. Mention the change in the commit message (`feat(skills): ...` / `fix(skills): ...`).
