"""
🚀 MediaEnhanceAI - Unified GUI Launcher
Launch Audio or Video Enhancer from a single entry point.

Usage:
    python run_gui.py           # Opens launcher menu
    python run_gui.py --audio   # Direct to Audio Enhancer
    python run_gui.py --video   # Direct to Video Enhancer
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def launch_audio_gui():
    """Launch the Audio Enhancer GUI."""
    from audio_enhancer.gui import ModernAudioCleanerGUI
    app = ModernAudioCleanerGUI()
    app.mainloop()


def launch_video_gui():
    """Launch the Video Enhancer GUI."""
    from video_enhancer.gui import ModernVideoEnhancerGUI
    app = ModernVideoEnhancerGUI()
    app.mainloop()


def show_launcher():
    """Show the launcher menu to choose between Audio and Video."""
    try:
        import customtkinter as ctk
    except ImportError:
        print("❌ customtkinter not found. Install with: pip install customtkinter")
        print("\nAlternatively, run directly:")
        print("  python -m audio_enhancer.gui")
        print("  python -m video_enhancer.gui")
        return

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Create launcher window
    root = ctk.CTk()
    root.title("MediaEnhanceAI Launcher")
    root.geometry("500x400")
    root.resizable(False, False)

    # Colors
    colors = {
        'bg': '#0f0f0f',
        'card': '#1a1a1a',
        'accent_audio': '#3B8ED0',
        'accent_video': '#9C27B0',
        'text': '#FAFAFA',
        'text_dim': '#9E9E9E'
    }

    root.configure(fg_color=colors['bg'])

    # Main container
    main = ctk.CTkFrame(root, fg_color="transparent")
    main.pack(fill="both", expand=True, padx=30, pady=30)

    # Title
    ctk.CTkLabel(
        main,
        text="🚀 MediaEnhanceAI",
        font=("Segoe UI", 32, "bold"),
        text_color=colors['text']
    ).pack(pady=(0, 5))

    ctk.CTkLabel(
        main,
        text="AI-Powered Media Enhancement Suite",
        font=("Segoe UI", 14),
        text_color=colors['text_dim']
    ).pack(pady=(0, 30))

    # Buttons container
    btn_frame = ctk.CTkFrame(main, fg_color="transparent")
    btn_frame.pack(fill="x", pady=10)

    def launch_audio():
        root.destroy()
        launch_audio_gui()

    def launch_video():
        root.destroy()
        launch_video_gui()

    # Audio Button
    audio_btn = ctk.CTkButton(
        btn_frame,
        text="🎵 Audio Enhancer",
        font=("Segoe UI", 18, "bold"),
        fg_color=colors['accent_audio'],
        hover_color="#2d7ab8",
        height=70,
        command=launch_audio
    )
    audio_btn.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(
        btn_frame,
        text="Noise reduction • Normalization • Format conversion",
        font=("Segoe UI", 11),
        text_color=colors['text_dim']
    ).pack(pady=(0, 20))

    # Video Button
    video_btn = ctk.CTkButton(
        btn_frame,
        text="🎬 Video Enhancer",
        font=("Segoe UI", 18, "bold"),
        fg_color=colors['accent_video'],
        hover_color="#7B1FA2",
        height=70,
        command=launch_video
    )
    video_btn.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(
        btn_frame,
        text="Upscaling • Denoising • Sharpening • Color correction",
        font=("Segoe UI", 11),
        text_color=colors['text_dim']
    ).pack()

    # Footer
    ctk.CTkLabel(
        main,
        text="Free & Open Source | MIT License",
        font=("Segoe UI", 10),
        text_color="#666666"
    ).pack(side="bottom", pady=(20, 0))

    root.mainloop()


def main():
    """Main entry point with CLI argument support."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--audio', '-a', 'audio']:
            print("🎵 Launching Audio Enhancer...")
            launch_audio_gui()
        elif arg in ['--video', '-v', 'video']:
            print("🎬 Launching Video Enhancer...")
            launch_video_gui()
        elif arg in ['--help', '-h']:
            print(__doc__)
        else:
            print(f"Unknown option: {arg}")
            print("Use --help for usage information.")
    else:
        show_launcher()


if __name__ == "__main__":
    main()
