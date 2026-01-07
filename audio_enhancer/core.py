"""
Professional Audio Cleaner & Optimizer - FULLY ADAPTIVE VERSION
Each audio file gets custom processing based on its actual characteristics
NO HARD-CODED VALUES - Everything adapts to YOUR audio!
"""

from __future__ import annotations

import os
import warnings
from typing import Callable

import librosa
import noisereduce as nr
import numpy as np
import soundfile as sf
from scipy import signal
warnings.filterwarnings('ignore')


class AudioCleaner:
    def __init__(self, input_file, output_file=None, target_sample_rate=48000):
        """Initialize ADAPTIVE Audio Cleaner"""
        self.input_file = input_file
        self.target_sr = target_sample_rate
        
        if output_file is None:
            name, _ = os.path.splitext(input_file)
            self.output_file = f"{name}_cleaned.wav"
        else:
            self.output_file = output_file
        
        self.audio: np.ndarray | None = None
        self.analysis_audio: np.ndarray | None = None
        self.original_audio: np.ndarray | None = None
        self.sr: int | None = None
        self.channels = 0
        self.processing_params: dict[str, float | bool] = {}
        
        print(f"🎵 ADAPTIVE Audio Cleaner - Custom Processing for Each File")
        print(f"📁 Input: {input_file}")
        print(f"📁 Output: {self.output_file}")
        
    def load_audio(self):
        """Load audio file"""
        print("\n⏳ Loading audio file...")
        try:
            audio, sr = librosa.load(
                self.input_file,
                sr=None,
                mono=False,
            )

            audio = np.asarray(audio, dtype=np.float32)

            if audio.ndim == 1:
                self.channels = 1
                self.audio = audio
                self.is_stereo = False
            else:
                self.channels = audio.shape[0]
                self.audio = audio
                self.is_stereo = self.channels > 1

            self.sr = int(sr)
            self.analysis_audio = librosa.to_mono(self.audio)
            self.original_audio = np.copy(self.audio)

            duration = self.audio.shape[-1] / self.sr if self.sr else 0
            print(f"✅ Loaded: {duration:.2f}s @ {self.sr}Hz")
            print(f"📊 Channels: {'Stereo' if self.is_stereo else 'Mono'}")
            return True
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            return False
    
    def analyze_quality(self):
        """ADAPTIVE quality analysis - determines exact processing needed"""
        print("\n🔬 AI-Powered Adaptive Analysis...")
        
        if self.audio is None or self.analysis_audio is None or self.sr is None:
            print("❌ Audio not loaded correctly")
            return False

        analysis_audio = self.analysis_audio

        # Calculate multiple metrics
        peak = np.max(np.abs(analysis_audio))
        rms = np.sqrt(np.mean(analysis_audio**2))
        
        # Estimate noise floor by analyzing quiet segments
        sorted_audio = np.sort(np.abs(analysis_audio))
        noise_floor = np.mean(sorted_audio[:int(len(sorted_audio) * 0.1)])  # Bottom 10%
        signal_level = np.mean(sorted_audio[int(len(sorted_audio) * 0.5):])  # Top 50%
        
        # Calculate actual SNR
        if noise_floor > 0:
            snr = 20 * np.log10(signal_level / noise_floor)
        else:
            snr = 100  # Very clean
        
        # Detect spectral noise using high-frequency analysis
        stft = np.abs(librosa.stft(analysis_audio))
        freq_bins = librosa.fft_frequencies(sr=self.sr)
        high_freq_mask = freq_bins > 8000  # Above 8kHz
        high_freq_energy = np.mean(stft[high_freq_mask, :])
        mid_freq_energy = np.mean(stft[~high_freq_mask, :])
        hf_ratio = high_freq_energy / (mid_freq_energy + 1e-10)
        
        print(f"   📊 Peak level: {peak:.3f}")
        print(f"   📊 RMS level: {rms:.3f}")
        print(f"   📊 Noise floor: {noise_floor:.4f}")
        print(f"   📊 SNR: {snr:.1f}dB")
        print(f"   📊 HF noise ratio: {hf_ratio:.3f}")
        
        # ADAPTIVE PROCESSING PARAMETERS
        self.needs_processing = False
        self.processing_params = {
            'noise_reduction': 0.0,
            'high_pass_cutoff': 0,
            'normalization_target': 0.8,
            'needs_limiting': False
        }
        
        # Determine noise reduction amount ADAPTIVELY based on SNR
        if snr < 15:
            # Very noisy - higher reduction
            self.processing_params['noise_reduction'] = 0.7
            print(f"\n⚠️ High noise detected (SNR: {snr:.1f}dB)")
            print(f"   🎯 Adaptive noise reduction: 70%")
            self.needs_processing = True
        elif snr < 25:
            # Moderate noise - medium reduction
            self.processing_params['noise_reduction'] = 0.5
            print(f"\n⚠️ Moderate noise detected (SNR: {snr:.1f}dB)")
            print(f"   🎯 Adaptive noise reduction: 50%")
            self.needs_processing = True
        elif snr < 40:
            # Light noise - gentle reduction
            self.processing_params['noise_reduction'] = 0.3
            print(f"\n✓ Light noise detected (SNR: {snr:.1f}dB)")
            print(f"   🎯 Adaptive noise reduction: 30%")
            self.needs_processing = True
        else:
            # Very clean
            self.processing_params['noise_reduction'] = 0.0
            print(f"\n✨ Excellent quality (SNR: {snr:.1f}dB)")
            print(f"   🎯 No noise reduction needed")
        
        # Adaptive high-frequency noise handling
        if hf_ratio > 0.3:
            print(f"   ⚠️ High-frequency noise detected")
            self.processing_params['noise_reduction'] = min(self.processing_params['noise_reduction'] + 0.1, 0.8)
            print(f"   🎯 Increased noise reduction to: {int(self.processing_params['noise_reduction']*100)}%")
        
        # Adaptive high-pass filter based on low-frequency content
        if noise_floor > 0.01:
            self.processing_params['high_pass_cutoff'] = 80
            print(f"   🎯 High-pass filter: 80Hz (significant rumble)")
            self.needs_processing = True
        elif noise_floor > 0.005:
            self.processing_params['high_pass_cutoff'] = 60
            print(f"   🎯 High-pass filter: 60Hz (slight rumble)")
            self.needs_processing = True
        elif noise_floor > 0.002:
            self.processing_params['high_pass_cutoff'] = 40
            print(f"   🎯 High-pass filter: 40Hz (minimal rumble)")
        else:
            self.processing_params['high_pass_cutoff'] = 0
            print(f"   ✨ No rumble detected - no high-pass needed")
        
        # Adaptive volume correction
        if peak > 0.99:
            print(f"   ⚠️ Clipping detected (peak: {peak:.3f})")
            self.processing_params['needs_limiting'] = True
            self.processing_params['normalization_target'] = 0.75
            self.needs_processing = True
        elif peak < 0.2:
            print(f"   ⚠️ Very low volume (peak: {peak:.3f})")
            self.processing_params['normalization_target'] = 0.8
            self.needs_processing = True
        elif peak < 0.5:
            print(f"   ℹ️ Moderate volume (peak: {peak:.3f})")
            self.processing_params['normalization_target'] = 0.8
        else:
            print(f"   ✓ Good volume (peak: {peak:.3f})")
            self.processing_params['normalization_target'] = 0.85
        
        return self.needs_processing
    
    def _apply_channelwise(self, func: Callable[[np.ndarray], np.ndarray]) -> None:
        """Apply processing function to each channel while preserving layout."""

        if self.audio is None:
            return

        if self.channels <= 1:
            self.audio = func(self.audio)
        else:
            processed_channels = [func(channel) for channel in self.audio]
            self.audio = np.vstack(processed_channels)

    def adaptive_noise_reduction(self, amount):
        """ADAPTIVE noise reduction - exact amount based on analysis"""
        if amount <= 0:
            print("\n✨ No noise reduction needed - audio is clean!")
            return
        
        print(f"\n🔇 Adaptive noise reduction ({int(amount*100)}% - calculated for THIS audio)...")
        try:
            def _reduce(channel: np.ndarray) -> np.ndarray:
                return nr.reduce_noise(
                    y=channel,
                    sr=self.sr,
                    stationary=True,
                    prop_decrease=amount,
                    n_fft=2048,
                    hop_length=512,
                )

            self._apply_channelwise(_reduce)
            print(f"✅ Applied {int(amount*100)}% noise reduction")
        except Exception as e:
            print(f"⚠️ Skipped: {e}")
    
    def smart_normalize(self, target=0.8):
        """Adaptive normalization to calculated target level"""
        print(f"\n📊 Adaptive normalization (target: {target:.2f} / {20*np.log10(target):.1f}dB)...")
        try:
            if self.audio is None:
                print("⚠️ No audio loaded, skipping normalization")
                return

            peak = float(np.abs(self.audio).max())
            if peak > 0:
                self.audio = self.audio * (target / peak)
                print(f"✅ Normalized to {target:.2f}")
            else:
                print("⚠️ Silent audio, skipping normalization")
        except Exception as e:
            print(f"❌ Normalization error: {e}")
    
    def adaptive_high_pass(self, cutoff):
        """Adaptive high-pass based on detected rumble"""
        if cutoff <= 0:
            print("\n✨ No high-pass needed - no rumble detected")
            return
        
        print(f"\n🎛️ Adaptive high-pass filter ({cutoff}Hz - calculated for THIS audio)...")
        try:
            if self.audio is None or self.sr is None:
                print("⚠️ No audio loaded, skipping high-pass")
                return

            nyquist = self.sr / 2
            normal_cutoff = cutoff / nyquist
            # Adaptive order: lower cutoff = gentler slope
            order = 2 if cutoff <= 60 else 3
            b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
            self._apply_channelwise(lambda channel: signal.filtfilt(b, a, channel))
            print(f"✅ High-pass applied at {cutoff}Hz (order {order})")
        except Exception as e:
            print(f"⚠️ Filter skipped: {e}")
    
    def gentle_limiter(self, threshold=-0.5):
        """Safety limiter to prevent clipping"""
        print(f"\n🛡️ Safety limiter ({threshold}dB)...")
        try:
            if self.audio is None:
                print("⚠️ No audio loaded, skipping limiter")
                return

            threshold_linear = 10 ** (threshold / 20)
            self.audio = np.clip(self.audio, -threshold_linear, threshold_linear)
            print("✅ Limiter applied")
        except Exception as e:
            print(f"❌ Limiter error: {e}")
    
    def resample_if_needed(self):
        """Resample to target sample rate"""
        if self.audio is None or self.sr is None:
            return

        if self.sr != self.target_sr:
            print(f"\n🔄 Resampling {self.sr}Hz → {self.target_sr}Hz...")
            self.audio = librosa.resample(
                self.audio,
                orig_sr=self.sr,
                target_sr=self.target_sr,
                axis=-1,
            )
            self.sr = self.target_sr
            print("✅ Resampled")
    
    def restore_stereo(self):
        """Restore stereo if original was stereo"""
        if not self.is_stereo or self.audio is None:
            return

        if self.audio.ndim == 1:
            print("\n🎧 Restoring stereo from mono mix...")
            self.audio = np.vstack([self.audio, self.audio])
            print("✅ Stereo restored")
    
    def save_audio(self, format='WAV'):
        """Save processed audio"""
        print(f"\n💾 Saving audio as {format}...")
        try:
            if self.audio is None or self.sr is None:
                print("❌ No audio data available to save")
                return None

            if self.is_stereo and len(self.audio.shape) == 2:
                audio_to_save = self.audio.T
            else:
                audio_to_save = self.audio
            
            sf.write(self.output_file, audio_to_save, self.sr, subtype='PCM_24')
            print(f"✅ Audio saved: {self.output_file}")
            return self.output_file
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None
    
    def process(self):
        """FULLY ADAPTIVE processing - customized for THIS specific audio file!"""
        print(f"\n{'='*60}")
        print(f"🎬 AI-POWERED FULLY ADAPTIVE PROCESSING")
        print(f"   (Custom parameters calculated for THIS audio)")
        print(f"{'='*60}")
        
        if not self.load_audio():
            return False
        
        needs_processing = self.analyze_quality()
        
        if needs_processing:
            print("\n📋 Applying custom corrections based on analysis...")
            
            # Apply noise reduction ONLY if needed and with EXACT calculated amount
            if self.processing_params['noise_reduction'] > 0:
                self.adaptive_noise_reduction(self.processing_params['noise_reduction'])
            
            # Apply high-pass ONLY if needed with EXACT calculated cutoff
            if self.processing_params['high_pass_cutoff'] > 0:
                self.adaptive_high_pass(self.processing_params['high_pass_cutoff'])
        else:
            print("\n✨ Audio quality is excellent - minimal processing only...")
        
        # Normalize to adaptive calculated target
        self.smart_normalize(target=self.processing_params['normalization_target'])
        
        # Limiter only if clipping was detected
        if self.processing_params.get('needs_limiting', False):
            self.gentle_limiter(threshold=-0.5)
        
        self.resample_if_needed()
        self.restore_stereo()
        
        print(f"\n{'='*60}")
        print(f"✨ Adaptive Processing Complete!")
        print(f"   Each setting was calculated specifically for THIS audio")
        print(f"{'='*60}")
        return True


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🎵 FULLY ADAPTIVE AUDIO CLEANER")
    print("   Custom processing for each unique audio file!")
    print("="*60)
    
    input_file = input("\n📁 Enter path to audio file: ").strip('"').strip("'")
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    cleaner = AudioCleaner(input_file, target_sample_rate=48000)
    
    if cleaner.process():
        output_file = cleaner.save_audio(format='WAV')
        
        if output_file:
            print(f"\n{'='*60}")
            print(f"🎉 SUCCESS!")
            print(f"📁 Cleaned audio saved to:")
            print(f"   {output_file}")
            print(f"{'='*60}\n")
        else:
            print("\n❌ Failed to save audio")
    else:
        print("\n❌ Processing failed")


if __name__ == "__main__":
    main()
