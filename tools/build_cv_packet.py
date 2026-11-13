"""Build an application PDF: the rendered CV followed by full-page image appendices (e.g. a transcript).

The appendix images and the output stay outside the public repo by default.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import typst
import tyro
import yaml
from icecream import ic
from pypdf import PdfWriter

ic.configureOutput(includeContext=True)

SITE_ROOT = Path(__file__).resolve().parent.parent
PRIVATE_DIR = SITE_ROOT.parent / "private"

APPENDIX_PAGE = """
#page(
  paper: "a4",
  margin: (x: 1.5cm, top: 2cm, bottom: 1.2cm),
  header: text(font: "New Computer Modern", size: 10pt)[*{title}* #h(1fr) {name} #h(1em) {index}/{count}],
)[#image("{image}", width: 100%, height: 100%, fit: "contain")]
"""


@dataclass
class Args:
    cv_file: Path = SITE_ROOT / "_data" / "cv.yml"
    appendix_images: tuple[Path, ...] = (
        PRIVATE_DIR / "transcript_p1.jpg",
        PRIVATE_DIR / "transcript_p2.jpg",
    )
    """One full page per image, in this order."""
    appendix_title: str = "Appendix: Academic Transcript (Undergraduate), KAIST"
    output: Path = PRIVATE_DIR / "Yoontae_Cho_CV_with_transcript.pdf"


def render_cv(cv_file: Path, pdf_path: Path) -> None:
    # rendercv resolves --pdf-path relative to the input file
    relative_pdf = os.path.relpath(pdf_path, cv_file.parent)
    subprocess.run(
        [sys.executable, "-m", "rendercv", "render", str(cv_file), "--pdf-path", relative_pdf, "--quiet"],
        check=True,
    )


def render_appendix(args: Args, name: str, work_dir: Path, pdf_path: Path) -> None:
    pages = []
    for index, image in enumerate(args.appendix_images, start=1):
        # typst only reads files under the directory of its source file
        local_image = work_dir / f"appendix_{index}{image.suffix}"
        shutil.copy(image, local_image)
        pages.append(
            APPENDIX_PAGE.format(
                title=args.appendix_title,
                name=name,
                index=index,
                count=len(args.appendix_images),
                image=local_image.name,
            )
        )
    source = work_dir / "appendix.typ"
    source.write_text("\n".join(pages))
    typst.compile(str(source), output=str(pdf_path))


def main(args: Args) -> None:
    name = yaml.safe_load(args.cv_file.read_text())["cv"]["name"]
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        cv_pdf = work_dir / "cv.pdf"
        appendix_pdf = work_dir / "appendix.pdf"
        render_cv(args.cv_file, cv_pdf)
        render_appendix(args, name, work_dir, appendix_pdf)

        writer = PdfWriter()
        writer.append(str(cv_pdf))
        writer.append(str(appendix_pdf))
        writer.write(str(args.output))

    page_count = len(writer.pages)
    size_mb = args.output.stat().st_size / 1e6
    msg = f"{args.output} ({page_count} pages, {size_mb:.1f} MB)"
    ic(msg)


if __name__ == "__main__":
    main(tyro.cli(Args))
