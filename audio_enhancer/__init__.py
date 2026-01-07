"""
🎵 Audio Enhancer Module
AI-powered adaptive audio cleaning and enhancement.

Usage:
    from audio_enhancer import AudioCleaner
    
    cleaner = AudioCleaner("input.mp3")
    cleaner.process()
    cleaner.save_audio()
"""

from .core import AudioCleaner

__version__ = "0.2.0"
__author__ = "MediaEnhanceAI"
__all__ = ["AudioCleaner"]
