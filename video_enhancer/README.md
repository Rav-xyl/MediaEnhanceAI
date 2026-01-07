# Video Enhancer

Adaptive denoising, sharpening, upscaling, and color correction through the `VideoEnhancer` class.

## Capabilities

- Inspects representative frames to quantify sharpness, noise, brightness, and contrast.
- Chooses denoise, sharpen, and color adjustments automatically based on analysis.
- Offers optional upscaling targets (auto analysis, 1080p, 4K).
- Streams enhancement frame-by-frame with OpenCV for reliability.

## Installation

Install from the project root:

```bash
pip install .
```

Optional tooling for development:

```bash
pip install .[dev]
```

## Command Line

```bash
# Enhance a single video and keep the output alongside the source
mediaenhance-video input.mp4

# Force 1080p output and write results to build/video
mediaenhance-video clips/ --target-resolution 1080p --output-dir build/video

# Preview the actions without writing any files
mediaenhance-video input.mp4 --dry-run
```

## Python API

```python
from video_enhancer import VideoEnhancer

enhancer = VideoEnhancer("input.mp4", target_resolution=(1920, 1080))

if enhancer.process():
   print("Enhanced video saved to", enhancer.output_file)
```

## Development

Run the video-specific regression test:

```bash
pytest tests/test_video_enhancer.py
```

Refer to the repository `CONTRIBUTING.md` for coding standards and review expectations.
