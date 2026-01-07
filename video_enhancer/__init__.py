"""
🎬 Video Enhancer Module
AI-powered adaptive video quality enhancement.

Usage:
    from video_enhancer import VideoEnhancer
    
    enhancer = VideoEnhancer("input.mp4", target_resolution=(1920, 1080))
    enhancer.process()
"""

from .core import VideoEnhancer

__version__ = "0.2.0"
__author__ = "MediaEnhanceAI"
__all__ = ["VideoEnhancer"]
