#!/usr/bin/env python3
"""Build a fully self-contained, offline HTML view of architecture_playbook.md.

The .md is the source of truth; this generates architecture_playbook.html as a
rendered view. The HTML embeds the markdown (base64) plus mermaid.js and marked.js
(inlined from tools/vendor/), so it opens in any browser with no network and no
extensions. Never hand-edit the HTML — edit the .md and re-run this script:

    python3 tools/build_playbook_html.py

Stdlib only; nothing to pip install.
"""
import base64
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
MD = ROOT / "architecture_playbook.md"
OUT = ROOT / "architecture_playbook.html"
MERMAID = (HERE / "vendor" / "mermaid.min.js").read_text(encoding="utf-8")
MARKED = (HERE / "vendor" / "marked.min.js").read_text(encoding="utf-8")

md_text = MD.read_text(encoding="utf-8")
md_b64 = base64.b64encode(md_text.encode("utf-8")).decode("ascii")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Architecture Playbook — SAP-RPT-1 in Action</title>
<script>%(MARKED)s</script>
<script>%(MERMAID)s</script>
<style>
  :root {
    --ink:#1d2d3e; --muted:#556b82; --line:#d5dadd; --accent:#0070f2;
    --bg:#ffffff; --soft:#f5f6f7; --code:#f5f6f7; --sap-sky:#ebf8ff;
  }
  * { box-sizing:border-box; }
  html { scroll-behavior:smooth; }
  body {
    margin:0; background:var(--soft); color:var(--ink);
    font:16px/1.65 "72","72 Brand",Arial,Helvetica,sans-serif;
  }
  .wrap { max-width:1180px; margin:0 auto; padding:48px 42px 120px; background:var(--bg);
          box-shadow:0 0 0 1px var(--line); }
  h1 { font-size:2rem; line-height:1.2; margin:.2em 0 .4em; letter-spacing:-.01em; }
  h2 { font-size:1.5rem; margin:2.2em 0 .5em; padding-top:.6em; border-top:2px solid #89d1ff; }
  h3 { font-size:1.18rem; margin:1.8em 0 .4em; color:#26324a; }
  h4 { font-size:1rem; margin:1.4em 0 .3em; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }
  p, li { color:#222836; }
  a { color:var(--accent); text-decoration:none; }
  a:hover { text-decoration:underline; }
  hr { border:0; border-top:1px solid var(--line); margin:2.4em 0; }
  code { background:var(--code); padding:.12em .38em; border-radius:4px; font-size:.9em;
         font-family:"SF Mono",Menlo,Consolas,monospace; }
  pre > code { display:block; padding:14px 16px; overflow-x:auto; }
  blockquote { margin:1.2em 0; padding:.6em 1.1em; border-left:4px solid var(--accent);
               background:var(--soft); color:#2a3140; border-radius:0 6px 6px 0; }
  table { border-collapse:collapse; width:100%%; margin:1.2em 0; font-size:.92rem; }
  th, td { border:1px solid var(--line); padding:9px 12px; text-align:left; vertical-align:top; }
  th { background:var(--sap-sky); font-weight:600; }
  tr:nth-child(even) td { background:#fbfcfe; }
  .mermaid { background:#fff; border:1px solid #89d1ff; border-radius:16px;
             padding:24px; margin:1.5em 0; text-align:center; overflow-x:auto;
             /* Metrically-stable font so Mermaid's label measurement matches
                what the browser paints — the "72" brand font is often not
                installed on the viewer's machine, which caused box text to clip. */
             font-family:Arial,Helvetica,sans-serif; }
  .mermaid svg { display:block; width:100%% !important; max-width:100%% !important; height:auto; margin:0 auto; }
  .mermaid p { margin:0 !important; line-height:1.25 !important; }
  .mermaid .nodeLabel, .mermaid .edgeLabel, .mermaid .cluster-label {
    line-height:1.25 !important;
  }
  .doc-banner { background:linear-gradient(90deg,#eaf3fd,#f7f9fc); border:1px solid #d3e2f5;
                border-radius:8px; padding:12px 16px; margin:0 0 26px; font-size:.9rem; color:#33465f; }
  .doc-banner b { color:var(--accent); }
  .toolbar { position:sticky; top:0; z-index:5; background:rgba(255,255,255,.92);
             backdrop-filter:blur(6px); border-bottom:1px solid var(--line);
             padding:8px 28px; display:flex; gap:14px; align-items:center; font-size:.82rem; }
  .toolbar button { border:1px solid var(--line); background:#fff; border-radius:6px;
                    padding:5px 11px; cursor:pointer; font-size:.82rem; color:var(--ink); }
  .toolbar button:hover { border-color:var(--accent); color:var(--accent); }
  .toolbar .sp { flex:1; }
  @media (max-width:760px) {
    .wrap { padding:30px 18px 80px; }
    table { display:block; overflow-x:auto; white-space:normal; }
    .mermaid { padding:12px; }
  }
  @media print {
    .toolbar { display:none; }
    .wrap { max-width:none; padding:20px; box-shadow:none; }
    body { background:#fff; }
    .mermaid { break-inside:avoid; }
  }
</style>
</head>
<body>
<div class="toolbar">
  <strong>Architecture Playbook</strong>
  <span class="sp"></span>
  <button onclick="window.print()">Print / Save as PDF</button>
</div>
<div class="wrap">
  <div class="doc-banner">
    Rendered view of <b>architecture_playbook.md</b>. Diagrams and tables render offline in this file —
    no extensions or internet required. The Markdown file remains the source of truth.
  </div>
  <div id="content">Rendering…</div>
</div>
<script>
  const MD_B64 = "%(MD_B64)s";
  const raw = decodeURIComponent(escape(atob(MD_B64)));

  // Custom renderer: emit ```mermaid fences as <pre class="mermaid"> for mermaid.js,
  // leave all other code blocks as normal highlighted code.
  const renderer = new marked.Renderer();
  const origCode = renderer.code.bind(renderer);
  renderer.code = (code, lang) => {
    if ((lang || "").trim() === "mermaid") {
      return '<pre class="mermaid">' + code + '</pre>';
    }
    return origCode(code, lang);
  };
  marked.setOptions({ renderer, gfm:true, breaks:false });

  document.getElementById("content").innerHTML = marked.parse(raw);

  mermaid.initialize({
    startOnLoad:false,
    theme:"base",
    securityLevel:"loose",
    themeVariables:{
      fontFamily:"Arial, Helvetica, sans-serif",
      fontSize:"16px",
      primaryColor:"#EBF8FF",
      primaryTextColor:"#1D2D3E",
      primaryBorderColor:"#0070F2",
      lineColor:"#556B82",
      secondaryColor:"#F5F6F7",
      tertiaryColor:"#FFFFFF",
      clusterBkg:"#EBF8FF",
      clusterBorder:"#0070F2",
      edgeLabelBackground:"#FFFFFF"
    },
    flowchart:{
      useMaxWidth:true,
      htmlLabels:true,
      curve:"stepAfter",
      nodeSpacing:52,
      rankSpacing:58,
      padding:24
    }
  });
  mermaid.run({ querySelector:".mermaid" });
</script>
</body>
</html>
""" % {"MARKED": MARKED, "MERMAID": MERMAID, "MD_B64": md_b64}

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT}  ({len(HTML):,} bytes)")
print(f"embedded markdown: {len(md_text):,} chars -> {len(md_b64):,} b64 chars")
