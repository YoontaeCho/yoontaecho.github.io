# yoontaecho.github.io

Personal site and CV of Yoontae Cho, built on the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. The CV PDF is rendered with [RenderCV](https://rendercv.com).

## Where things live

| To change                     | Edit                                                                 |
| ----------------------------- | -------------------------------------------------------------------- |
| CV (PDF and the `/cv/` page)  | `_data/cv.yml`                                                       |
| CV look (theme, page, colors) | `design:` block at the bottom of `_data/cv.yml`                      |
| Figures on the `/cv/` page    | `image:` on an entry in `_data/cv.yml` (logos in `assets/img/logo/`) |
| Publications page             | `_bibliography/papers.bib`, thumbnails in `assets/img/publication_preview/` |
| Project pages                 | `_projects/*.md`                                                     |
| Bio and photo                 | `_pages/about.md`, `assets/img/prof_pic.jpg`                         |
| Email and social icons        | `_data/socials.yml`                                                  |
| Video clips                   | `tools/media.yaml`                                                   |

A new paper goes in two places: `_bibliography/papers.bib` for the site and the `Publications` section of `_data/cv.yml` for the CV.

## Commands

Build the website PDF, `assets/pdf/Yoontae_Cho_CV.pdf`: the CV followed by the transcript pages in `_cv_appendix/`. Those pages are public, so they must stay the redacted copies (student ID, birth date, degree number, verification number and barcode blacked out):

```bash
uv run python tools/build_cv_packet.py public
```

Build the application PDF with the unredacted transcript. Its images and output stay outside this repo, in `../private/`:

```bash
uv run python tools/build_cv_packet.py private
uv run python tools/build_cv_packet.py private --appendix-images a.jpg b.jpg --output ../private/packet.pdf
```

Render the CV alone to `.rendercv/Yoontae_Cho_CV.pdf`, or try another RenderCV theme without touching the file:

```bash
uv run rendercv render _data/cv.yml
uv run rendercv render _data/cv.yml --design.theme harvard
```

Convert raw recordings into web clips. Originals stay outside this repo (default: the parent folder), and each entry in `tools/media.yaml` becomes `assets/video/<name>.mp4` plus a poster at `assets/img/<name>.jpg`:

```bash
uv run python tools/process_media.py
uv run python tools/process_media.py --only humanoid_hurdle --crf 24
```

Embed a clip in a page with `{% include clip.liquid name="humanoid_hurdle" caption="Hurdle crossing" %}`.

Preview the site at <http://localhost:8080>:

```bash
docker compose up -d
docker compose down
```

## Deploying

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the website PDF (the `public` preset above), builds the site and publishes it to the `gh-pages` branch. The PDF is not committed; it is regenerated from `_data/cv.yml` and `_cv_appendix/` on every deploy.
