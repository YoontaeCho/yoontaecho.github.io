"""Convert raw recordings into small, muted, metadata-free web clips plus poster frames."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import tyro
import yaml
from icecream import ic

ic.configureOutput(includeContext=True)

SITE_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Clip:
    name: str
    src: str
    start: float | None = None
    end: float | None = None
    crop: str | None = None
    poster_time: float = 0.0


@dataclass
class Args:
    raw_dir: Path = SITE_ROOT.parent
    """Folder holding the original recordings (kept outside the public repo)."""
    clips_file: Path = SITE_ROOT / "tools" / "media.yaml"
    only: tuple[str, ...] = ()
    """Clip names to process; empty means all."""
    height: int = 720
    """Maximum output height; smaller sources are not upscaled."""
    fps: int = 30
    crf: int = 26
    """x264 quality: lower is sharper and larger."""
    poster_width: int = 800


def run_ffmpeg(ffmpeg_args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ffmpeg_args], check=True)


def encode_clip(clip: Clip, args: Args) -> Path:
    src = args.raw_dir / clip.src
    out = SITE_ROOT / "assets" / "video" / f"{clip.name}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    trim = []
    if clip.start is not None:
        trim += ["-ss", str(clip.start)]
    if clip.end is not None:
        trim += ["-to", str(clip.end)]

    filters = []
    if clip.crop is not None:
        filters.append(f"crop={clip.crop}")
    filters += [f"scale=-2:'min(ih,{args.height})'", f"fps={args.fps}"]

    run_ffmpeg(
        [
            *trim,
            "-i", str(src),
            "-map", "0:v:0",
            "-vf", ",".join(filters),
            "-an",
            "-map_metadata", "-1",
            "-map_chapters", "-1",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", str(args.crf),
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(out),
        ]
    )
    return out


def extract_poster(clip: Clip, video: Path, args: Args) -> Path:
    out = SITE_ROOT / "assets" / "img" / f"{clip.name}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    run_ffmpeg(
        [
            "-ss", str(clip.poster_time),
            "-i", str(video),
            "-frames:v", "1",
            "-vf", f"scale={args.poster_width}:-2",
            "-q:v", "3",
            str(out),
        ]
    )
    return out


def main(args: Args) -> None:
    entries = yaml.safe_load(args.clips_file.read_text())["clips"]
    clips = [Clip(**entry) for entry in entries]
    if args.only:
        clips = [clip for clip in clips if clip.name in args.only]

    for clip in clips:
        video = encode_clip(clip, args)
        poster = extract_poster(clip, video, args)
        size_mb = video.stat().st_size / 1e6
        msg = f"{clip.name}: {video.relative_to(SITE_ROOT)} ({size_mb:.1f} MB), poster {poster.relative_to(SITE_ROOT)}"
        ic(msg)


if __name__ == "__main__":
    main(tyro.cli(Args))
