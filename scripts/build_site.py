#!/usr/bin/env python3
"""Render Jinja templates → HTML pages at the right paths."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent.parent
TEMPLATES = ROOT / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html"]),
    trim_blocks=False,
    lstrip_blocks=False,
)

# (template, output path, page metadata)
PAGES = [
    ("bio.html",      "index.html",            "bio",      "Bio",      "David Chelimo — Clinical Bioinformatics Scientist."),
    ("cv.html",       "cv/index.html",         "cv",       "CV",       "David Chelimo's CV — clinical bioinformatics, NGS, agentic coding."),
    ("projects.html", "projects/index.html",   "projects", "Projects", "Projects by David Chelimo — bioinformatics tooling and AI-assisted workflows."),
    ("blog.html",     "blog/index.html",       "blog",     "Blog",     "Writing by David Chelimo on clinical bioinformatics and agentic coding."),
]

def render_all():
    for template, output, active, title, description in PAGES:
        # Compute relative path from output back to root
        depth = output.count("/")
        root_rel = "../" * depth if depth else ""
        css_path = f"{root_rel}dist/styles.css"

        html = env.get_template(template).render(
            active=active,
            page_title=title,
            page_description=description,
            root=root_rel,
            css_path=css_path,
        )

        out_path = ROOT / output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  rendered {template:20s} → {output}")

if __name__ == "__main__":
    print("Building site:")
    render_all()
    print("Done.")
