#!/usr/bin/env python3
"""Generate David-Chelimo-Resume.pdf from cv/index.html + dist/styles.css using WeasyPrint."""

import re
from pathlib import Path
from weasyprint import HTML, CSS

ROOT = Path(__file__).parent.parent
HTML_FILE = ROOT / "cv" / "index.html"
CSS_FILE = ROOT / "dist" / "styles.css"
OUTPUT = ROOT / "David-Chelimo-Resume.pdf"

html_content = HTML_FILE.read_text(encoding="utf-8")

# Strip site nav and footer from the PDF (they're not part of the resume)
html_content = re.sub(r'<nav class="site-nav">.*?</nav>', "", html_content, flags=re.DOTALL)
html_content = re.sub(r'<footer class="site-footer">.*?</footer>', "", html_content, flags=re.DOTALL)

# Strip the on-screen contact button row (the resume header repeats the same info)
html_content = re.sub(r'<div class="header-links hero-links">.*?</div>', "", html_content, flags=re.DOTALL)

# Point stylesheet to absolute path for WeasyPrint
html_content = re.sub(
    r'href="(\.\./)*dist/styles\.css"',
    f'href="file://{CSS_FILE}"',
    html_content,
)

pdf_css = CSS(string="""
    @page {
        size: A4;
        margin: 12mm 14mm;
    }
    body::before { display: none; }
    .card { box-shadow: none !important; }
    details > div { display: block !important; }
    summary { display: none !important; }
""")

HTML(string=html_content, base_url=str(ROOT)).write_pdf(
    OUTPUT,
    stylesheets=[pdf_css]
)

print(f"PDF written to {OUTPUT}")
