# 📦 Examples

This folder contains example scripts demonstrating how to use MediaEnhanceAI programmatically.

## Available Examples

### batch_process.py
Batch process multiple audio and video files from a folder.

```bash
# Process all audio files in a folder
python batch_process.py --audio path/to/audio/folder

# Process all video files with 1080p output
python batch_process.py --video path/to/video/folder --resolution 1080p

# Process all media files (audio + video)
python batch_process.py path/to/media/folder

# Specify output folder
python batch_process.py --audio input/folder --output output/folder
```

## Quick Python Usage

### Audio Enhancement
```python
from audio_enhancer import AudioCleaner

cleaner = AudioCleaner("noisy_audio.mp3")
cleaner.process()
cleaner.save_audio()  # Saves as noisy_audio_cleaned.wav
```

### Video Enhancement
```python
from video_enhancer import VideoEnhancer

# Auto resolution (intelligent upscaling)
enhancer = VideoEnhancer("low_quality.mp4")
enhancer.process()

# Specific resolution
enhancer = VideoEnhancer("input.mp4", target_resolution=(1920, 1080))
enhancer.process()
```

## Tips

1. **Best Results**: Use high-quality source files when possible
2. **Batch Processing**: Use the CLI tool for processing many files
3. **Memory**: Large videos may require significant RAM
4. **GPU**: Video processing benefits from GPU acceleration (OpenCV CUDA)
