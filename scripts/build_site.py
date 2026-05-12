#!/usr/bin/env python3
"""Render Jinja templates → HTML pages at the right paths."""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent.parent
TEMPLATES = ROOT / "templates"
DATA = ROOT / "data"

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html"]),
    trim_blocks=False,
    lstrip_blocks=False,
)


def _normalize_bullet(b):
    """Bullets may be plain strings or {text, pdf?, web?} dicts.
    Return a uniform dict so templates iterate without branching."""
    if isinstance(b, str):
        return {"text": b, "pdf": True, "web": True}
    return {"text": b["text"], "pdf": b.get("pdf", True), "web": b.get("web", True)}


def load_cv():
    """Load data/cv.yaml and normalize bullet shapes."""
    data = yaml.safe_load((DATA / "cv.yaml").read_text(encoding="utf-8"))

    for entry in data.get("experience", []) + data.get("earlier_experience", []):
        entry["bullets"] = [_normalize_bullet(b) for b in entry.get("bullets", [])]

    for entry in data.get("selected_work", {}).get("entries", []) or []:
        entry["bullets"] = [_normalize_bullet(b) for b in entry.get("bullets", [])]

    return data


# (template, output path, page metadata)
PAGES = [
    ("bio.html",      "index.html",            "bio",      "Bio",      "David Chelimo — Clinical Bioinformatics Scientist."),
    ("cv.html",       "cv/index.html",         "cv",       "CV",       "David Chelimo's CV — clinical bioinformatics, NGS, agentic coding."),
    ("cv_print.html", "cv/print/index.html",   "cv",       "CV (Print)", "Print-only CV source used to generate the PDF."),
    ("projects.html", "projects/index.html",   "projects", "Projects", "Projects by David Chelimo — bioinformatics tooling and AI-assisted workflows."),
    ("blog.html",                       "blog/index.html",                       "blog", "Blog",                    "Writing by David Chelimo on clinical bioinformatics and agentic coding."),
    ("blog/building-this-site.html",         "blog/building-this-site/index.html",         "blog",     "Building This Site",          "How I built dchelimo.afyagateway.io using Claude Code, Jinja2, Tailwind, and WeasyPrint."),
    ("projects/benefits-pdf-analyzer.html",  "projects/benefits-pdf-analyzer/index.html",  "projects", "Benefits PDF Analyzer",       "A tool that compares employee benefits PDFs across organizations using AI-assisted extraction."),
]


def render_all():
    cv_data = load_cv()

    for template, output, active, title, description in PAGES:
        depth = output.count("/")
        root_rel = "../" * depth if depth else ""
        css_path = f"{root_rel}dist/styles.css"

        html = env.get_template(template).render(
            active=active,
            page_title=title,
            page_description=description,
            root=root_rel,
            css_path=css_path,
            cv=cv_data,
        )

        out_path = ROOT / output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  rendered {template:24s} → {output}")


if __name__ == "__main__":
    print("Building site:")
    render_all()
    print("Done.")
