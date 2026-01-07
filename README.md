<p align="center">
  <h1 align="center">🎬 MediaEnhanceAI</h1>
  <p align="center">
    <strong>AI-Powered Audio & Video Enhancement Suite</strong>
  </p>
  <p align="center">
    Free, open-source tools that automatically analyze and enhance your media files with adaptive AI processing.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-purple.svg" alt="GUI">
</p>

---

## ✨ Why MediaEnhanceAI?

| Feature | MediaEnhanceAI | Adobe Premiere | DaVinci Resolve |
|---------|----------------|----------------|-----------------|
| **Price** | ✅ **FREE** | ❌ $22/month | ⚠️ Free tier limited |
| **AI Adaptive** | ✅ Fully automatic | ⚠️ Manual presets | ⚠️ Manual presets |
| **Learning Curve** | ✅ One-click | ❌ Weeks to learn | ❌ Complex UI |
| **Batch Processing** | ✅ Built-in | ⚠️ Requires setup | ⚠️ Requires setup |
| **Open Source** | ✅ Yes | ❌ No | ❌ No |

---

## 🚀 Features

### 🎵 Audio Enhancer
- **Adaptive Noise Reduction** - Automatically detects and removes background noise
- **Smart Normalization** - Consistent volume levels across files
- **High-Pass Filtering** - Removes rumble and low-frequency noise
- **Stereo Preservation** - Maintains original channel layout
- **Multi-Format Support** - WAV, MP3, FLAC, M4A, OGG, AAC

### 🎬 Video Enhancer
- **Intelligent Upscaling** - LANCZOS4 algorithm (up to 4K)
- **Adaptive Denoising** - Frame-by-frame noise analysis
- **Smart Sharpening** - Enhances details without artifacts
- **Color Correction** - Automatic brightness, contrast, saturation
- **Multi-Format Support** - MP4, AVI, MOV, MKV, WMV, FLV

---

## 📦 Installation

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/MediaEnhanceAI.git
cd MediaEnhanceAI

# Install the package
pip install .

# (Optional) Install developer tooling
pip install .[dev]
```

### Requirements
- Python 3.8+
- FFmpeg (for audio format conversion)

---

## 🎯 Quick Start

### Launch the GUI
```bash
# Run the unified launcher
python run_gui.py

# Or run individual tools
python -m audio_enhancer.gui    # Audio Enhancer
python -m video_enhancer.gui    # Video Enhancer
```

### Command Line
```bash
# Clean multiple audio files into a separate folder
mediaenhance-audio recordings/ --output-dir build/audio

# Enhance a video with automatic analysis and 1080p target resolution
mediaenhance-video sample.mp4 --target-resolution 1080p

# Launch the GUI directly from the command line
mediaenhance-gui
```

### Python API
```python
from audio_enhancer import AudioCleaner
from video_enhancer import VideoEnhancer

# Enhance audio
cleaner = AudioCleaner("input.mp3")
cleaner.process()
cleaner.save_audio()

# Enhance video
enhancer = VideoEnhancer("input.mp4", target_resolution=(1920, 1080))
enhancer.process()
```

---

## 📊 How It Works

### Audio Enhancement Pipeline
```
Input Audio → AI Analysis → Adaptive Processing → Enhanced Output
                  ↓
         ┌───────────────────┐
         │ • SNR Detection   │
         │ • Noise Floor     │
         │ • HF Analysis     │
         │ • Peak/RMS Levels │
         └───────────────────┘
```

### Video Enhancement Pipeline
```
Input Video → Frame Sampling → Quality Analysis → Adaptive Enhancement
                                     ↓
                    ┌────────────────────────────┐
                    │ • Resolution Check         │
                    │ • Noise Level Measurement  │
                    │ • Sharpness Analysis       │
                    │ • Brightness/Contrast      │
                    │ • Color Analysis           │
                    └────────────────────────────┘
```

---

## 📁 Project Structure

```
MediaEnhanceAI/
├── README.md               # This file
├── LICENSE                 # MIT License
├── requirements.txt        # Pinned dependency mirror
├── pyproject.toml          # Packaging metadata and dependencies
├── run_gui.py              # Unified GUI launcher
│
├── .github/workflows/      # Continuous integration
│   └── ci.yml
│
├── audio_enhancer/         # Audio processing module
│   ├── core.py             # AudioCleaner class
│   ├── gui.py              # Modern GUI
│   ├── cli.py              # Command-line entry point
│   └── README.md           # Audio-specific docs
│
├── video_enhancer/         # Video processing module
│   ├── core.py             # VideoEnhancer class
│   ├── gui.py              # Modern GUI
│   ├── cli.py              # Command-line entry point
│   └── README.md           # Video-specific docs
│
├── examples/               # Usage examples
│   └── batch_process.py
│
└── tests/                  # Automated regression tests
  ├── test_audio_cleaner.py
  └── test_video_enhancer.py
```

---

## 🖥️ GUI Preview

Both tools feature a modern, dark-themed interface built with CustomTkinter:

- 📁 **Drag & Drop** file selection
- 📊 **Real-time Progress** tracking
- 📝 **Terminal Output** with syntax highlighting
- ⚙️ **Customizable Settings** per file type

---

## ⚡ Performance

| Operation | Speed | Notes |
|-----------|-------|-------|
| Audio Analysis | ~1 sec | Per file |
| Audio Processing | ~2-5 sec | Depends on length |
| Video Analysis | ~2-3 sec | 20 frame samples |
| Video Processing | 10-30 FPS | Depends on resolution |

---

## 🛠️ Configuration

### Audio Settings
| Parameter | Default | Description |
|-----------|---------|-------------|
| Sample Rate | 48kHz | Output sample rate |
| Noise Reduction | Auto | 0-70% based on analysis |
| High-Pass Filter | Auto | 40-80Hz based on rumble |

### Video Settings
| Parameter | Options | Description |
|-----------|---------|-------------|
| Resolution | Auto, 1080p, 4K, Original | Target output resolution |
| Denoising | Auto | 0-10 based on noise level |
| Sharpening | Auto | 0-1.5 based on blur analysis |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

📍 **Check out our [ROADMAP.md](ROADMAP.md)** for planned features you can help implement!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) - Computer vision library
- [Librosa](https://librosa.org/) - Audio analysis
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework
- [noisereduce](https://github.com/timsainb/noisereduce) - Noise reduction algorithms

---

<p align="center">
  Made with ❤️ for content creators who deserve professional-quality tools for free.
</p>
