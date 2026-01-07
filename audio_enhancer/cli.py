"""Command line entry point for the adaptive audio cleaner."""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable

from .core import AudioCleaner


def _iter_audio_files(paths: Iterable[str]) -> Iterable[pathlib.Path]:
    """Yield audio files, expanding directories one level deep."""
    for path_str in paths:
        path = pathlib.Path(path_str).expanduser().resolve()
        if path.is_dir():
            for candidate in sorted(path.iterdir()):
                if candidate.is_file():
                    yield candidate
        elif path.is_file():
            yield path
        else:
            raise FileNotFoundError(f"No such file or directory: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean audio files using adaptive analysis and enhancement",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="One or more audio files or directories to process",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=None,
        help="Optional directory for processed output (defaults to alongside the input)",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=48_000,
        help="Target sample rate for the enhanced audio (default: 48000)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would be processed without writing outputs",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        files = list(_iter_audio_files(args.inputs))
    except FileNotFoundError as exc:  # pragma: no cover - argparse message
        parser.error(str(exc))
        return 2

    if not files:
        parser.error("No audio files found to process")
        return 2

    output_root = args.output_dir
    if output_root is not None:
        output_root.mkdir(parents=True, exist_ok=True)

    for file_path in files:
        destination = None
        if output_root is not None:
            destination = output_root / f"{file_path.stem}_cleaned.wav"

        cleaner = AudioCleaner(
            input_file=str(file_path),
            output_file=str(destination) if destination is not None else None,
            target_sample_rate=args.sample_rate,
        )

        if args.dry_run:
            print(f"[DRY-RUN] Would process {file_path}")
            continue

        if not cleaner.process():
            print(f"Failed to process {file_path}", file=sys.stderr)
            return 1
        if cleaner.save_audio(format="WAV") is None:
            print(f"Failed to save processed audio for {file_path}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
