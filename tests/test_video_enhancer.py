"""Basic integration tests for the adaptive video enhancer."""

from __future__ import annotations

import pathlib

import cv2
import numpy as np

from video_enhancer import VideoEnhancer


def _write_fixture(tmp_path: pathlib.Path) -> pathlib.Path:
    width, height = 64, 64
    frames = 12
    fps = 8

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    file_path = tmp_path / "sample.mp4"
    writer = cv2.VideoWriter(str(file_path), fourcc, fps, (width, height))

    for idx in range(frames):
        value = (idx * 20) % 255
        frame = np.full((height, width, 3), value, dtype=np.uint8)
        writer.write(frame)

    writer.release()
    return file_path


def test_video_enhancer_enhances(tmp_path: pathlib.Path) -> None:
    input_path = _write_fixture(tmp_path)
    output_path = tmp_path / "enhanced.mp4"

    enhancer = VideoEnhancer(str(input_path), output_file=str(output_path), target_resolution=(128, 128))
    assert enhancer.process() is True

    assert output_path.exists()
    assert output_path.stat().st_size > 0
