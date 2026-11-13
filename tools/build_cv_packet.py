"""Build a PDF of the rendered CV followed by full-page image appendices (e.g. a transcript).

Presets:
  public   website PDF, using the redacted transcript pages kept in _cv_appendix/
  private  application PDF with the unredacted pages; inputs and output stay outside the repo
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import typst
import tyro
from icecream import ic
from pypdf import PdfWriter

ic.configureOutput(includeContext=True)

SITE_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_APPENDIX_DIR = SITE_ROOT / "_cv_appendix"
PRIVATE_DIR = SITE_ROOT.parent / "private"

# title, note and image are inserted as typst string literals
APPENDIX_PAGE = """
#page(
  paper: "a4",
  margin: (x: 1.5cm, top: 2cm, bottom: 1.2cm),
  header: text(font: "New Computer Modern", size: 10pt)[
    #strong({title}) #h(0.6em) #{note} #h(1fr) {index}/{count}
  ],
)[#image({image}, width: 100%, height: 100%, fit: "contain")]
"""


@dataclass
class Args:
    appendix_images: tuple[Path, ...]
    """One full page per image, in this order."""
    output: Path
    appendix_title: str = "Appendix: Academic Transcript (Undergraduate), KAIST"
    appendix_note: str = ""
    """Shown after the title in regular weight."""
    cv_file: Path = SITE_ROOT / "_data" / "cv.yml"


PRESETS = {
    "public": (
        "Website PDF: CV plus the redacted transcript pages kept in the repo.",
        Args(
            appendix_images=(
                PUBLIC_APPENDIX_DIR / "transcript_p1.jpg",
                PUBLIC_APPENDIX_DIR / "transcript_p2.jpg",
            ),
            output=SITE_ROOT / "assets" / "pdf" / "Yoontae_Cho_CV.pdf",
            appendix_note="(personal identifiers redacted)",
        ),
    ),
    "private": (
        "Application PDF: CV plus the unredacted transcript, kept outside the repo.",
        Args(
            appendix_images=(
                PRIVATE_DIR / "transcript_p1.jpg",
                PRIVATE_DIR / "transcript_p2.jpg",
            ),
            output=PRIVATE_DIR / "Yoontae_Cho_CV_with_transcript.pdf",
        ),
    ),
}


def typst_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_cv(cv_file: Path, pdf_path: Path) -> None:
    # rendercv resolves --pdf-path relative to the input file
    relative_pdf = os.path.relpath(pdf_path, cv_file.parent)
    subprocess.run(
        [sys.executable, "-m", "rendercv", "render", str(cv_file), "--pdf-path", relative_pdf, "--quiet"],
        check=True,
    )


def render_appendix(args: Args, work_dir: Path, pdf_path: Path) -> None:
    pages = []
    for index, image in enumerate(args.appendix_images, start=1):
        # typst only reads files under the directory of its source file
        local_image = work_dir / f"appendix_{index}{image.suffix}"
        shutil.copy(image, local_image)
        pages.append(
            APPENDIX_PAGE.format(
                title=typst_string(args.appendix_title),
                note=typst_string(args.appendix_note),
                index=index,
                count=len(args.appendix_images),
                image=typst_string(local_image.name),
            )
        )
    source = work_dir / "appendix.typ"
    source.write_text("\n".join(pages))
    typst.compile(str(source), output=str(pdf_path))


def main(args: Args) -> None:
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        cv_pdf = work_dir / "cv.pdf"
        appendix_pdf = work_dir / "appendix.pdf"
        render_cv(args.cv_file, cv_pdf)
        render_appendix(args, work_dir, appendix_pdf)

        writer = PdfWriter()
        writer.append(str(cv_pdf))
        writer.append(str(appendix_pdf))
        writer.write(str(args.output))

    page_count = len(writer.pages)
    size_mb = args.output.stat().st_size / 1e6
    msg = f"{args.output} ({page_count} pages, {size_mb:.1f} MB)"
    ic(msg)


if __name__ == "__main__":
    main(tyro.extras.overridable_config_cli(PRESETS))
