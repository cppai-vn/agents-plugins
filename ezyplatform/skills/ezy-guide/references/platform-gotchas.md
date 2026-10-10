# EzyPlatform gotchas (verified)

Each entry was observed against a live server. Keep the evidence line; when a
gotcha stops reproducing on a newer platform version, update or remove it via
the improvement loop.

| # | Behaviour | Consequence / rule | Evidence |
|---|---|---|---|
| 1 | Cloudflare in front of the admin API returns `403 error 1010` for the default `Python-urllib` User-Agent. | Always send an explicit User-Agent (`ezy_client.py` does). | cpp.ai.vn, 2026-10-10 |
| 2 | `GET /ezyarticle/api/v1/pages/{page}/fragments/{name}` ignores `?i18n_lang=`; it always returns the default language. | Read a localized fragment through `GET /ezyarticle/api/v1/posts/{id}?i18n_lang=<lang>`. Otherwise a "sync" overwrites `content.en.html` with Vietnamese. | header/footer `.en` compare, 2026-10-10 |
| 3 | `PUT /ezyarticle/api/v1/posts/{id}` answers `400 {"fields":"invalid"}` when the body contains `metadata`, `terms`, `priority`, `publishedAt`, `parentId` or `commentStatus`. | Omit them; stored values are kept. Rebuild the body from the live post (`ezy_client.update_payload`). | theme no-op PUT, 2026-10-10 |
| 4 | Localized writes need `"language": "<lang>"` in the PUT body; without it the default language is overwritten. | Publish each language as its own request. | home vi/en publish |
| 5 | The server stores one `summary` for all languages; `meta.<lang>.json` summary is not persisted. | Put localized SEO text in the localized HTML `<meta>` tags instead. | home en summary compare |
| 6 | A fragment linked to a menu (e.g. header → menu 1) keeps the link only if `menuId` is sent; extension 0.2.8 does not send it from `meta.json`. | Publish such fragments with `ezy-publish` (keeps `menuId` from the live post), not the extension, until the extension supports it. | header post 10 |
| 7 | `GET /api/v1/settings/web-url` returns plain text, not JSON. | Use `ezy_client.request_text`. | 2026-10-10 |
| 8 | `/api/v1/media/<name>` on the public site returns 404 until the file is uploaded to the media library; local `api/v1/media` files are not on the server by themselves. | Run `ezy-media status` before referencing a media URL. | cpp.ai.vn, 2026-10-10 |
| 9 | Page/fragment `contentType` must be `THYMELEAF` for `ezy:replace`, `th:*`, `ezyfunctions` or `#messages` to render; `HTML` outputs them verbatim. | Check `meta.json` when markup shows up raw on the live page (`ezy-verify live` flags it). | README notes |
| 10 | Embedding images as data URLs works but bloats every page (cpp.ai.vn home ≈385 KB) and duplicates them per language. | Prefer the media library + `?v=` / `ezy:mhref`. | cpp.ai.vn home |
| 11 | Scroll-driven CSS animations (`animation-timeline: view()`) leave elements half transparent while partly in view. | Avoid opacity-based scroll reveals on content. | cpp.ai.vn redesign review |
| 12 | No admin API to list pages was found (fragments have `/pages/fragments`). | Pages must be pulled by slug; `ezy-sync pull-all` only refreshes pages already present locally. | ezy-sync pull-all build, 2026-10-10 |
