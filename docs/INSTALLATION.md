# 📚 Documentation

## Installation Guide

### Prerequisites

- **Python 3.8+** - Download from [python.org](https://www.python.org)
- **FFmpeg** - Required for audio format conversion

### Installing FFmpeg

#### Windows
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH environment variable

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

### Installing MediaEnhanceAI

```bash
# Clone the repository
git clone https://github.com/yourusername/MediaEnhanceAI.git
cd MediaEnhanceAI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install .
```

---

## API Reference

### AudioCleaner

```python
from audio_enhancer import AudioCleaner

cleaner = AudioCleaner(
    input_file: str,           # Path to input audio file
    output_file: str = None,   # Output path (optional)
    target_sample_rate: int = 48000  # Target sample rate
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `load_audio()` | Load the input audio file |
| `analyze_quality()` | Analyze and determine processing parameters |
| `process()` | Run full adaptive processing pipeline |
| `save_audio(format='WAV')` | Save processed audio |

### VideoEnhancer

```python
from video_enhancer import VideoEnhancer

enhancer = VideoEnhancer(
    input_file: str,              # Path to input video file
    output_file: str = None,      # Output path (optional)
    target_resolution: tuple = None  # (width, height) or None for auto
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `analyze_video()` | Analyze video quality and determine enhancements |
| `enhance_frame(frame)` | Apply enhancements to a single frame |
| `process()` | Run full adaptive processing pipeline |

---

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "FFmpeg not found" error
Ensure FFmpeg is installed and in your system PATH.

### Audio sounds over-processed
The processing is adaptive, but for already clean audio, it applies minimal changes.

### Video processing is slow
- Processing speed depends on resolution and enhancements needed
- Consider using a lower target resolution for faster processing
- GPU acceleration can help (requires OpenCV with CUDA)
