"""Basic integration tests for the adaptive audio cleaner."""

from __future__ import annotations

import pathlib

import numpy as np
import soundfile as sf

from audio_enhancer import AudioCleaner


def _write_fixture(tmp_path: pathlib.Path) -> pathlib.Path:
    sample_rate = 22050
    seconds = 1.0
    t = np.linspace(0, seconds, int(sample_rate * seconds), endpoint=False)
    tone = 0.2 * np.sin(2 * np.pi * 440 * t)
    noise = 0.02 * np.random.default_rng(42).standard_normal(size=tone.shape)
    audio = tone + noise

    input_path = tmp_path / "noisy.wav"
    sf.write(input_path, audio, sample_rate)
    return input_path


def test_audio_cleaner_enhances_and_saves(tmp_path: pathlib.Path) -> None:
    input_path = _write_fixture(tmp_path)
    cleaner = AudioCleaner(str(input_path), target_sample_rate=44100)

    assert cleaner.process() is True
    output_path = cleaner.save_audio(format="WAV")
    assert output_path is not None

    saved = pathlib.Path(output_path)
    assert saved.exists()

    data, sr = sf.read(saved)
    assert sr == 44100
    assert data.size > 0
