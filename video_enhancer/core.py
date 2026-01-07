"""
AI-Powered Adaptive Video Quality Enhancer
Analyzes each video and applies custom enhancements
Upscaling, denoising, sharpening, color correction - all adaptive!
"""

import os
import cv2
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class VideoEnhancer:
    def __init__(self, input_file, output_file=None, target_resolution=None):
        """
        Initialize Adaptive Video Enhancer
        
        Args:
            input_file: Path to input video
            output_file: Path to output (optional)
            target_resolution: Target resolution tuple (width, height) or None for auto
        """
        self.input_file = input_file
        self.target_resolution = target_resolution
        
        if output_file is None:
            name, ext = os.path.splitext(input_file)
            self.output_file = f"{name}_enhanced{ext}"
        else:
            self.output_file = output_file
        
        self.cap = None
        self.enhancement_params = {}
        
        print(f"🎬 ADAPTIVE Video Quality Enhancer")
        print(f"📁 Input: {input_file}")
        print(f"📁 Output: {self.output_file}")
    
    def analyze_video(self):
        """Analyze video quality and determine enhancements needed"""
        print("\n🔬 Analyzing video quality...")
        
        self.cap = cv2.VideoCapture(self.input_file)
        
        if not self.cap.isOpened():
            print("❌ Cannot open video file")
            return False
        
        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Validate properties - some codecs don't report correctly
        if self.frame_count <= 0 or self.fps <= 0:
            print("   ⚠️ Video metadata incomplete, counting frames manually...")
            # Count frames manually
            frame_count = 0
            while True:
                ret, _ = self.cap.read()
                if not ret:
                    break
                frame_count += 1
            self.frame_count = frame_count
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            # Estimate FPS if not available
            if self.fps <= 0:
                self.fps = 30.0  # Assume 30 FPS
                print(f"   ⚠️ FPS not detected, assuming 30 FPS")
        
        if self.frame_count <= 0:
            print("❌ No frames found in video")
            return False
        
        self.duration = self.frame_count / self.fps if self.fps > 0 else 0
        
        print(f"   📊 Resolution: {self.width}x{self.height}")
        print(f"   📊 FPS: {self.fps:.2f}")
        print(f"   📊 Duration: {self.duration:.2f}s")
        print(f"   📊 Total frames: {self.frame_count}")
        
        # Sample frames for quality analysis
        print("\n🔍 Sampling frames for quality analysis...")
        sample_indices = np.linspace(0, self.frame_count - 1, min(20, self.frame_count), dtype=int)
        
        brightness_values = []
        contrast_values = []
        sharpness_values = []
        noise_levels = []
        
        for idx in sample_indices:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = self.cap.read()
            
            if not ret:
                continue
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Brightness
            brightness = np.mean(gray)
            brightness_values.append(brightness)
            
            # Contrast
            contrast = np.std(gray)
            contrast_values.append(contrast)
            
            # Sharpness (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            sharpness_values.append(sharpness)
            
            # Noise estimation
            noise = self._estimate_noise(gray)
            noise_levels.append(noise)
        
        # Calculate average metrics
        avg_brightness = np.mean(brightness_values)
        avg_contrast = np.mean(contrast_values)
        avg_sharpness = np.mean(sharpness_values)
        avg_noise = np.mean(noise_levels)
        
        print(f"   📊 Avg Brightness: {avg_brightness:.1f}/255")
        print(f"   📊 Avg Contrast: {avg_contrast:.1f}")
        print(f"   📊 Avg Sharpness: {avg_sharpness:.1f}")
        print(f"   📊 Avg Noise: {avg_noise:.3f}")
        
        # ADAPTIVE ENHANCEMENT PARAMETERS
        self.enhancement_params = {
            'needs_upscaling': False,
            'upscale_factor': 1.0,
            'denoise_strength': 0,
            'sharpen_amount': 0.0,
            'brightness_adjust': 0,
            'contrast_adjust': 1.0,
            'color_enhance': False
        }
        
        # Determine upscaling
        if self.target_resolution:
            target_w, target_h = self.target_resolution
            if self.width < target_w or self.height < target_h:
                self.enhancement_params['needs_upscaling'] = True
                self.enhancement_params['upscale_factor'] = max(target_w / self.width, target_h / self.height)
                print(f"\n🎯 Upscaling needed: {self.enhancement_params['upscale_factor']:.2f}x")
        else:
            # Auto-detect if resolution is low
            if self.width < 1280 or self.height < 720:
                self.enhancement_params['needs_upscaling'] = True
                if self.width < 640:
                    self.enhancement_params['upscale_factor'] = 2.0
                    print(f"\n🎯 Low resolution detected - 2x upscaling recommended")
                else:
                    self.enhancement_params['upscale_factor'] = 1.5
                    print(f"\n🎯 Medium resolution - 1.5x upscaling recommended")
        
        # Adaptive denoising
        if avg_noise > 15:
            self.enhancement_params['denoise_strength'] = 10
            print(f"   🎯 High noise detected - Strong denoising (10)")
        elif avg_noise > 8:
            self.enhancement_params['denoise_strength'] = 5
            print(f"   🎯 Moderate noise - Medium denoising (5)")
        elif avg_noise > 4:
            self.enhancement_params['denoise_strength'] = 3
            print(f"   🎯 Light noise - Gentle denoising (3)")
        else:
            print(f"   ✨ Clean video - No denoising needed")
        
        # Adaptive sharpening
        if avg_sharpness < 100:
            self.enhancement_params['sharpen_amount'] = 1.5
            print(f"   🎯 Blurry video - Strong sharpening (1.5)")
        elif avg_sharpness < 300:
            self.enhancement_params['sharpen_amount'] = 0.8
            print(f"   🎯 Soft video - Medium sharpening (0.8)")
        elif avg_sharpness < 500:
            self.enhancement_params['sharpen_amount'] = 0.3
            print(f"   🎯 Slight softness - Gentle sharpening (0.3)")
        else:
            print(f"   ✨ Sharp video - No sharpening needed")
        
        # Adaptive brightness/contrast
        if avg_brightness < 80:
            self.enhancement_params['brightness_adjust'] = 30
            print(f"   🎯 Dark video - Brightness +30")
        elif avg_brightness > 180:
            self.enhancement_params['brightness_adjust'] = -20
            print(f"   🎯 Bright video - Brightness -20")
        
        if avg_contrast < 30:
            self.enhancement_params['contrast_adjust'] = 1.3
            print(f"   🎯 Low contrast - Contrast 1.3x")
        elif avg_contrast < 50:
            self.enhancement_params['contrast_adjust'] = 1.15
            print(f"   🎯 Moderate contrast - Contrast 1.15x")
        
        # Color enhancement for dull videos
        if avg_contrast < 40:
            self.enhancement_params['color_enhance'] = True
            print(f"   🎯 Dull colors - Color enhancement enabled")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to start
        return True
    
    def _estimate_noise(self, gray_frame):
        """Estimate noise level in frame"""
        h, w = gray_frame.shape
        # Use central region
        center = gray_frame[h//4:3*h//4, w//4:3*w//4]
        # High-pass filter to isolate noise
        blur = cv2.GaussianBlur(center, (5, 5), 0)
        noise = center.astype(float) - blur.astype(float)
        return np.std(noise)
    
    def enhance_frame(self, frame):
        """Apply adaptive enhancements to a single frame"""
        
        # 1. Denoising (if needed)
        if self.enhancement_params['denoise_strength'] > 0:
            frame = cv2.fastNlMeansDenoisingColored(
                frame, 
                None,
                h=self.enhancement_params['denoise_strength'],
                hColor=self.enhancement_params['denoise_strength'],
                templateWindowSize=7,
                searchWindowSize=21
            )
        
        # 2. Upscaling (if needed)
        if self.enhancement_params['needs_upscaling']:
            factor = self.enhancement_params['upscale_factor']
            new_width = int(frame.shape[1] * factor)
            new_height = int(frame.shape[0] * factor)
            # Use LANCZOS for best quality upscaling
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        
        # 3. Sharpening (if needed)
        if self.enhancement_params['sharpen_amount'] > 0:
            amount = self.enhancement_params['sharpen_amount']
            # Unsharp mask
            gaussian = cv2.GaussianBlur(frame, (0, 0), 2.0)
            frame = cv2.addWeighted(frame, 1.0 + amount, gaussian, -amount, 0)
        
        # 4. Brightness adjustment
        if self.enhancement_params['brightness_adjust'] != 0:
            frame = cv2.convertScaleAbs(frame, alpha=1, beta=self.enhancement_params['brightness_adjust'])
        
        # 5. Contrast adjustment
        if self.enhancement_params['contrast_adjust'] != 1.0:
            frame = cv2.convertScaleAbs(frame, alpha=self.enhancement_params['contrast_adjust'], beta=0)
        
        # 6. Color enhancement
        if self.enhancement_params['color_enhance']:
            # Convert to HSV and enhance saturation
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(float)
            hsv[:, :, 1] = hsv[:, :, 1] * 1.2  # Increase saturation by 20%
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        return frame
    
    def process(self):
        """Process video with adaptive enhancements"""
        print(f"\n{'='*60}")
        print(f"🎬 Starting Adaptive Video Enhancement")
        print(f"{'='*60}")
        
        if not self.analyze_video():
            return False
        
        # Determine output codec and settings
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Output dimensions
        if self.enhancement_params['needs_upscaling']:
            out_width = int(self.width * self.enhancement_params['upscale_factor'])
            out_height = int(self.height * self.enhancement_params['upscale_factor'])
        else:
            out_width = self.width
            out_height = self.height
        
        print(f"\n📤 Output settings:")
        print(f"   Resolution: {out_width}x{out_height}")
        print(f"   FPS: {self.fps:.2f}")
        
        # Create video writer
        out = cv2.VideoWriter(self.output_file, fourcc, self.fps, (out_width, out_height))
        
        if not out.isOpened():
            print("❌ Cannot create output video")
            return False
        
        print(f"\n🎥 Processing frames...")
        frame_num = 0
        
        while True:
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            # Enhance frame
            enhanced_frame = self.enhance_frame(frame)
            
            # Write frame
            out.write(enhanced_frame)
            
            frame_num += 1
            
            # Progress indicator
            if frame_num % 30 == 0:
                progress = (frame_num / self.frame_count) * 100
                print(f"   Progress: {progress:.1f}% ({frame_num}/{self.frame_count} frames)", end='\r')
        
        print(f"\n✅ Processed {frame_num} frames                              ")
        
        # Cleanup
        self.cap.release()
        out.release()
        
        print(f"\n{'='*60}")
        print(f"✨ Video Enhancement Complete!")
        print(f"{'='*60}")
        print(f"📁 Enhanced video saved: {self.output_file}")
        
        return True


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🎬 AI-POWERED ADAPTIVE VIDEO QUALITY ENHANCER")
    print("   Custom enhancements calculated for each video!")
    print("="*60)
    
    input_file = input("\n📁 Enter path to video file: ").strip('"').strip("'")
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    # Ask for target resolution
    print("\n📐 Target resolution:")
    print("  1. Auto (intelligent upscaling if needed)")
    print("  2. 1080p (1920x1080)")
    print("  3. 4K (3840x2160)")
    print("  4. Keep original")
    
    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"
    
    target_res = None
    if choice == '2':
        target_res = (1920, 1080)
    elif choice == '3':
        target_res = (3840, 2160)
    
    enhancer = VideoEnhancer(input_file, target_resolution=target_res)
    
    if enhancer.process():
        print(f"\n🎉 SUCCESS!")
    else:
        print(f"\n❌ Enhancement failed")


if __name__ == "__main__":
    main()
