# Audio Enhancer

Adaptive, analysis-driven audio cleanup built around the `AudioCleaner` class.

## Feature Highlights

- Adaptive spectral noise reduction with automatic strength selection.
- Intelligent high-pass filtering that reacts to measured rumble.
- Loudness normalization with clipping protection.
- Optional resampling to consistent sample rates for publishing workflows.
- Stereo-aware processing that preserves channel separation.

## Installation

Install the project from the repository root:

```bash
pip install .
```

Developer dependencies (linting, tests) live behind the `dev` extra:

```bash
pip install .[dev]
```

## Command Line

Use the packaged entry point to clean one or many audio files:

```bash
# Process every file in recordings/ and place results in build/audio
mediaenhance-audio recordings/ --output-dir build/audio

# Keep outputs next to the source file
mediaenhance-audio sample.wav

# Preview without writing any files
mediaenhance-audio sample.wav --dry-run
```

## Python API

```python
from audio_enhancer import AudioCleaner

cleaner = AudioCleaner("voiceover.mp3", target_sample_rate=48000)

if cleaner.process():
    cleaner.save_audio()
```

## Development

Run the automated regression test:

```bash
pytest tests/test_audio_cleaner.py
```

Community contributions are welcome—see the repository `CONTRIBUTING.md` for expectations.
