# dsc_bio

Personal site for David Chelimo, live at **[dchelimo.afyagateway.io](https://dchelimo.afyagateway.io)**.

## Stack

- **Templating:** Jinja2 → static HTML
- **Styles:** Tailwind CSS v3 (compiled via CLI)
- **PDF résumé:** WeasyPrint, generated from the CV page
- **CI:** GitHub Actions builds CSS, HTML, and PDF on every push to `main`
- **Hosting:** GitHub Pages, custom domain via `CNAME`

## Pages

| Path | Content |
|---|---|
| `/` | Bio (landing) |
| `/cv/` | Full CV |
| `/projects/` | Projects (placeholder) |
| `/blog/` | Blog (placeholder) |

## Local development

```bash
# Install
npm install
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Edit templates in templates/, then:
.venv/bin/python scripts/build_site.py    # render Jinja → HTML
npm run build:css                         # compile Tailwind → dist/styles.css
.venv/bin/python scripts/generate_pdf.py  # regenerate the PDF résumé
```

Don't edit the generated HTML files (`index.html`, `cv/index.html`, etc.) directly — edit the templates in `templates/` instead.

See [`CLAUDE.md`](./CLAUDE.md) for more detail on the build pipeline and design tokens.
