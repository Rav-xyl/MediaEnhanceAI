"""Command line interface for the adaptive video enhancer."""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable

from .core import VideoEnhancer

_RESOLUTION_MAP = {
    "auto": None,
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


def _iter_video_files(paths: Iterable[str]) -> Iterable[pathlib.Path]:
    """Yield video files, expanding directories recursively."""
    for path_str in paths:
        path = pathlib.Path(path_str).expanduser().resolve()
        if path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.is_file():
                    yield candidate
        elif path.is_file():
            yield path
        else:
            raise FileNotFoundError(f"No such file or directory: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Enhance video files with adaptive denoising, upscaling, and color correction",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="One or more video files or directories to process",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=None,
        help="Optional directory for enhanced videos (defaults to alongside the input)",
    )
    parser.add_argument(
        "--target-resolution",
        choices=sorted(_RESOLUTION_MAP.keys()),
        default="auto",
        help="Desired output resolution (auto analyses the input)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report planned operations without writing files",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        files = list(_iter_video_files(args.inputs))
    except FileNotFoundError as exc:  # pragma: no cover - argparse message
        parser.error(str(exc))
        return 2

    if not files:
        parser.error("No video files found to process")
        return 2

    output_root = args.output_dir
    if output_root is not None:
        output_root.mkdir(parents=True, exist_ok=True)

    resolution_option = _RESOLUTION_MAP[args.target_resolution]

    for file_path in files:
        destination = None
        if output_root is not None:
            destination = output_root / f"{file_path.stem}_enhanced{file_path.suffix}"

        enhancer = VideoEnhancer(
            input_file=str(file_path),
            output_file=str(destination) if destination is not None else None,
            target_resolution=resolution_option,
        )

        if args.dry_run:
            print(f"[DRY-RUN] Would process {file_path}")
            continue

        if not enhancer.process():
            print(f"Failed to process {file_path}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
