"""
📦 Batch Processing Example
Process multiple audio and video files with MediaEnhanceAI.

Usage:
    python batch_process.py --audio path/to/audio/folder
    python batch_process.py --video path/to/video/folder
    python batch_process.py --all path/to/media/folder
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def process_audio_folder(folder: str, output_folder: str = None):
    """
    Process all audio files in a folder.
    
    Args:
        folder: Path to folder containing audio files
        output_folder: Optional output folder (default: same as input)
    """
    from audio_enhancer import AudioCleaner
    
    audio_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'}
    folder_path = Path(folder)
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder}")
        return
    
    files = [f for f in folder_path.iterdir() 
             if f.suffix.lower() in audio_extensions]
    
    if not files:
        print(f"⚠️ No audio files found in {folder}")
        return
    
    print(f"🎵 Found {len(files)} audio files to process")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for i, input_file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {input_file.name}")
        
        try:
            if output_folder:
                output_path = Path(output_folder) / f"{input_file.stem}_cleaned.wav"
                cleaner = AudioCleaner(str(input_file), output_file=str(output_path))
            else:
                cleaner = AudioCleaner(str(input_file))
            
            if cleaner.process():
                cleaner.save_audio()
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Completed: {successful} successful, {failed} failed")


def process_video_folder(folder: str, output_folder: str = None, 
                         resolution: str = "auto"):
    """
    Process all video files in a folder.
    
    Args:
        folder: Path to folder containing video files
        output_folder: Optional output folder (default: same as input)
        resolution: Target resolution (auto, 1080p, 4k, original)
    """
    from video_enhancer import VideoEnhancer
    
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    folder_path = Path(folder)
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder}")
        return
    
    files = [f for f in folder_path.iterdir() 
             if f.suffix.lower() in video_extensions]
    
    if not files:
        print(f"⚠️ No video files found in {folder}")
        return
    
    # Determine target resolution
    target_res = None
    if resolution == "1080p":
        target_res = (1920, 1080)
    elif resolution == "4k":
        target_res = (3840, 2160)
    elif resolution != "original":
        target_res = None  # Auto
    
    print(f"🎬 Found {len(files)} video files to process")
    print(f"📐 Target resolution: {resolution}")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for i, input_file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {input_file.name}")
        
        try:
            if output_folder:
                output_path = Path(output_folder) / f"{input_file.stem}_enhanced{input_file.suffix}"
                enhancer = VideoEnhancer(str(input_file), output_file=str(output_path),
                                         target_resolution=target_res)
            else:
                enhancer = VideoEnhancer(str(input_file), target_resolution=target_res)
            
            if enhancer.process():
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Completed: {successful} successful, {failed} failed")


def main():
    parser = argparse.ArgumentParser(
        description="Batch process media files with MediaEnhanceAI"
    )
    parser.add_argument("folder", help="Folder containing media files")
    parser.add_argument("--audio", "-a", action="store_true", 
                        help="Process audio files only")
    parser.add_argument("--video", "-v", action="store_true",
                        help="Process video files only")
    parser.add_argument("--output", "-o", help="Output folder (optional)")
    parser.add_argument("--resolution", "-r", default="auto",
                        choices=["auto", "1080p", "4k", "original"],
                        help="Target video resolution")
    
    args = parser.parse_args()
    
    if args.audio:
        process_audio_folder(args.folder, args.output)
    elif args.video:
        process_video_folder(args.folder, args.output, args.resolution)
    else:
        # Process both
        print("🚀 Processing all media files...")
        print("\n" + "=" * 50)
        print("🎵 AUDIO FILES")
        print("=" * 50)
        process_audio_folder(args.folder, args.output)
        
        print("\n" + "=" * 50)
        print("🎬 VIDEO FILES")
        print("=" * 50)
        process_video_folder(args.folder, args.output, args.resolution)


if __name__ == "__main__":
    main()
