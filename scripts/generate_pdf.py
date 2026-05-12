#!/usr/bin/env python3
"""Generate David-Chelimo-Resume.pdf from cv/print/index.html + dist/styles.css using WeasyPrint."""

import re
from pathlib import Path
from weasyprint import HTML, CSS

ROOT = Path(__file__).parent.parent
HTML_FILE = ROOT / "cv" / "print" / "index.html"
CSS_FILE = ROOT / "dist" / "styles.css"
OUTPUT = ROOT / "David-Chelimo-Resume.pdf"

html_content = HTML_FILE.read_text(encoding="utf-8")

# Point the relative stylesheet href at the absolute path WeasyPrint can read.
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
""")

HTML(string=html_content, base_url=str(ROOT)).write_pdf(
    OUTPUT,
    stylesheets=[pdf_css]
)

print(f"PDF written to {OUTPUT}")
