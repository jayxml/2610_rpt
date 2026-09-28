# tools/ — playbook HTML build

Generates `architecture_playbook.html` (a self-contained, offline rendered view)
from `architecture_playbook.md` (the source of truth).

## Rebuild after editing the playbook

```bash
python3 tools/build_playbook_html.py
```

Stdlib only — nothing to install. The script inlines `vendor/mermaid.min.js` and
`vendor/marked.min.js` and base64-embeds the markdown, so the resulting HTML opens
in any browser with **no network and no extensions**, and every mermaid diagram and
table renders.

**Never hand-edit `architecture_playbook.html`** — edit the `.md` and re-run the build.

## Vendored libraries (`vendor/`)

Pinned, offline copies so the build is reproducible by anyone who clones the repo:

| File | Version | Source |
|------|---------|--------|
| `mermaid.min.js` | 10.9.1 | https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js |
| `marked.min.js`  | 12.0.2 | https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js |

To upgrade, re-download the pinned URL into `vendor/` and rebuild.
