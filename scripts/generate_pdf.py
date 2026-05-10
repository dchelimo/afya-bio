#!/usr/bin/env python3
"""Generate David-Chelimo-Resume.pdf from index.html + dist/styles.css using WeasyPrint."""

import re
from pathlib import Path
from weasyprint import HTML, CSS

ROOT = Path(__file__).parent.parent
HTML_FILE = ROOT / "index.html"
CSS_FILE = ROOT / "dist" / "styles.css"
OUTPUT = ROOT / "David-Chelimo-Resume.pdf"

html_content = HTML_FILE.read_text(encoding="utf-8")

# Remove the hero-links (buttons) and html2pdf script from the PDF
html_content = re.sub(r'<div class="hero-links[^"]*".*?</div>', "", html_content, flags=re.DOTALL)
html_content = re.sub(r'<script src="https://cdnjs[^<]+</script>', "", html_content)
html_content = re.sub(r'<script>\s*function downloadPDF.*?</script>', "", html_content, flags=re.DOTALL)

# Point stylesheet to absolute path for WeasyPrint
html_content = html_content.replace(
    'href="dist/styles.css"',
    f'href="file://{CSS_FILE}"'
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
