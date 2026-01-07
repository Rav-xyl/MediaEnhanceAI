"""
🎬 Professional Video Enhancer GUI
A beautiful, modern interface for the AI-Powered Adaptive Video Quality Enhancer
Uses customtkinter for a sleek dark mode experience

DEPENDENCY: pip install customtkinter opencv-python numpy
"""

import os
import sys
import threading
from io import StringIO
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Import the enhancer logic
try:
    from .core import VideoEnhancer
except ImportError:
    from core import VideoEnhancer

# --- THEME CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ModernVideoEnhancerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Video Enhancer Pro AI")
        self.geometry("1050x850")
        self.minsize(950, 750)
        
        # Color Palette (Dark Modern - Video themed)
        self.colors = {
            'bg': '#0f0f0f',           # Main Window BG (deeper dark)
            'card': '#1a1a1a',         # Card/Section BG
            'accent': '#9C27B0',       # Primary Purple (video-themed)
            'accent_hover': '#7B1FA2', # Darker purple for hover
            'success': '#00E676',      # Success Green (vibrant)
            'error': '#FF5252',        # Error Red
            'warning': '#FFD740',      # Warning Yellow
            'text': '#FAFAFA',         # Primary Text
            'text_dim': '#9E9E9E',     # Secondary Text
            'console_bg': '#121212',   # Console specific dark
            'border': '#333333'        # Border color
        }

        # Variables
        self.files_to_process = []
        self.output_folder = None
        self.is_processing = False
        self.target_resolution = tk.StringVar(value="auto")

        # Build UI
        self.configure(fg_color=self.colors['bg'])
        self.create_ui()

    def create_ui(self):
        """Create the modern card-based UI"""
        # Main container with padding
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # 1. Header Section
        self.create_header(main_frame)

        # 2. Workspace Area
        workspace = ctk.CTkFrame(main_frame, fg_color="transparent")
        workspace.pack(fill="both", expand=True)

        # Files Card
        self.create_file_section(workspace)
        
        # Settings Row (Resolution + Output Folder)
        settings_row = ctk.CTkFrame(workspace, fg_color="transparent")
        settings_row.pack(fill="x", pady=(0, 15))
        
        # Resolution Settings (Left side)
        self.create_resolution_section(settings_row)
        
        # Output Folder (Right side)
        self.create_output_section(settings_row)
        
        # Action Buttons Row
        self.create_action_section(workspace)

        # Progress & Console Card
        self.create_console_section(workspace)

    def create_header(self, parent):
        """Header with modern typography and gradient effect"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))

        # Left side - Title and badges
        left_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_section.pack(side="left")

        # Icon & Title
        title_label = ctk.CTkLabel(
            left_section, 
            text="🎬 Video Enhancer Pro", 
            font=("Segoe UI", 36, "bold"),
            text_color=self.colors['text']
        )
        title_label.pack(side="left")

        # AI Badge
        badge = ctk.CTkLabel(
            left_section,
            text=" AI POWERED ",
            font=("Segoe UI", 10, "bold"),
            fg_color=self.colors['accent'],
            text_color="white",
            corner_radius=8,
            height=26
        )
        badge.pack(side="left", padx=15, pady=5)

        # Subtitle
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Adaptive Upscaling • Denoising • Sharpening • Color Correction",
            font=("Segoe UI", 12),
            text_color=self.colors['text_dim']
        )
        subtitle.pack(side="right", padx=10)

    def create_file_section(self, parent):
        """File selection card with drag-drop style"""
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=16, border_width=1, border_color=self.colors['border'])
        card.pack(fill="x", pady=(0, 15))
        
        # Inner padding frame
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=18, fill="x")

        # Title Row
        top_row = ctk.CTkFrame(inner, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(
            top_row, 
            text="📁 INPUT VIDEO FILES", 
            font=("Segoe UI", 14, "bold"), 
            text_color=self.colors['text']
        ).pack(side="left")

        self.file_count_label = ctk.CTkLabel(
            top_row, 
            text="No files selected", 
            font=("Segoe UI", 12), 
            text_color=self.colors['text_dim']
        )
        self.file_count_label.pack(side="right")

        # Layout: Listbox on left, Buttons on right
        content_row = ctk.CTkFrame(inner, fg_color="transparent")
        content_row.pack(fill="x")

        # Custom Listbox Container
        list_container = ctk.CTkFrame(content_row, fg_color=self.colors['console_bg'], corner_radius=12, border_width=1, border_color=self.colors['border'])
        list_container.pack(side="left", fill="x", expand=True, ipady=5)

        self.file_listbox = tk.Listbox(
            list_container,
            height=5,
            bg=self.colors['console_bg'],
            fg=self.colors['text'],
            selectbackground=self.colors['accent'],
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            font=("Consolas", 11),
            activestyle='none'
        )
        self.file_listbox.pack(side="left", fill="both", expand=True, padx=12, pady=8)

        # Scrollbar for listbox
        scrollbar = ctk.CTkScrollbar(list_container, command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons Column
        btn_col = ctk.CTkFrame(content_row, fg_color="transparent")
        btn_col.pack(side="right", padx=(18, 0), fill="y")

        self.add_files_btn = ctk.CTkButton(
            btn_col, text="➕ Add Files", command=self.add_files, 
            width=130, height=38, fg_color=self.colors['accent'], hover_color=self.colors['accent_hover'],
            font=("Segoe UI", 12, "bold")
        )
        self.add_files_btn.pack(pady=(0, 10))

        self.add_folder_btn = ctk.CTkButton(
            btn_col, text="📂 Add Folder", command=self.add_folder, 
            width=130, height=38, fg_color="transparent", border_width=2, border_color=self.colors['accent'],
            hover_color="#2a1a30", font=("Segoe UI", 12)
        )
        self.add_folder_btn.pack(pady=(0, 10))

        self.clear_btn = ctk.CTkButton(
            btn_col, text="🗑️ Clear All", command=self.clear_files, 
            width=130, height=38, fg_color="transparent", text_color=self.colors['error'], 
            hover_color="#2a1515", font=("Segoe UI", 12)
        )
        self.clear_btn.pack(side="bottom")

    def create_resolution_section(self, parent):
        """Resolution selection card"""
        container = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=16, border_width=1, border_color=self.colors['border'])
        container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(padx=20, pady=18, fill="both")

        ctk.CTkLabel(
            inner, 
            text="📐 TARGET RESOLUTION", 
            font=("Segoe UI", 12, "bold"), 
            text_color=self.colors['text_dim']
        ).pack(anchor="w", pady=(0, 12))

        # Resolution options in a horizontal layout
        options_frame = ctk.CTkFrame(inner, fg_color="transparent")
        options_frame.pack(fill="x")

        resolution_options = [
            ("Auto", "auto", "Intelligent upscaling based on analysis"),
            ("1080p", "1080p", "1920 × 1080"),
            ("4K", "4k", "3840 × 2160"),
            ("Original", "original", "Keep source resolution")
        ]

        for label, value, tooltip in resolution_options:
            btn = ctk.CTkRadioButton(
                options_frame,
                text=f" {label}",
                variable=self.target_resolution,
                value=value,
                font=("Segoe UI", 12),
                fg_color=self.colors['accent'],
                hover_color=self.colors['accent_hover'],
                border_color=self.colors['text_dim']
            )
            btn.pack(side="left", padx=(0, 20))

    def create_output_section(self, parent):
        """Output folder selection"""
        container = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=16, border_width=1, border_color=self.colors['border'])
        container.pack(side="right", fill="both", expand=True, padx=(10, 0))

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(padx=20, pady=18, fill="both")

        ctk.CTkLabel(
            inner, 
            text="💾 OUTPUT DESTINATION", 
            font=("Segoe UI", 12, "bold"), 
            text_color=self.colors['text_dim']
        ).pack(anchor="w", pady=(0, 10))

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x")

        self.output_entry = ctk.CTkEntry(
            row, 
            placeholder_text="Default: Same as input", 
            height=38, 
            border_color=self.colors['border'],
            fg_color=self.colors['console_bg'],
            font=("Segoe UI", 11)
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.output_entry.insert(0, "Same as input folder (default)")
        self.output_entry.configure(state="disabled")

        ctk.CTkButton(
            row, text="Browse", width=80, height=38, 
            command=self.select_output_folder,
            fg_color=self.colors['accent'], hover_color=self.colors['accent_hover']
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            row, text="↺", width=38, height=38, 
            command=self.reset_output_folder, 
            fg_color="#404040", hover_color="#555555",
            font=("Segoe UI", 14)
        ).pack(side="left")

    def create_action_section(self, parent):
        """Start/Stop buttons in a centered row"""
        container = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=16, border_width=1, border_color=self.colors['border'])
        container.pack(fill="x", pady=(0, 15))

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(padx=20, pady=18)

        self.start_btn = ctk.CTkButton(
            inner, 
            text="🚀 START ENHANCEMENT", 
            font=("Segoe UI", 16, "bold"),
            command=self.start_processing,
            fg_color=self.colors['success'],
            hover_color="#00C853",
            text_color="#000000",
            height=55,
            width=280,
            corner_radius=12
        )
        self.start_btn.pack(side="left", padx=(0, 15))

        self.stop_btn = ctk.CTkButton(
            inner,
            text="⏹ STOP",
            font=("Segoe UI", 14, "bold"),
            command=self.stop_processing,
            fg_color=self.colors['error'],
            hover_color="#D32F2F",
            height=55,
            width=100,
            corner_radius=12,
            state="disabled"
        )
        self.stop_btn.pack(side="left")

    def create_console_section(self, parent):
        """Logs and Progress"""
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=16, border_width=1, border_color=self.colors['border'])
        card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both", expand=True)

        # Status Bar
        status_row = ctk.CTkFrame(inner, fg_color="transparent")
        status_row.pack(fill="x", pady=(0, 12))

        self.status_label = ctk.CTkLabel(
            status_row, 
            text="⏳ Ready to enhance videos", 
            font=("Segoe UI", 13), 
            text_color=self.colors['text']
        )
        self.status_label.pack(side="left")

        self.progress_percent = ctk.CTkLabel(
            status_row, 
            text="0%", 
            font=("Segoe UI", 14, "bold"), 
            text_color=self.colors['accent']
        )
        self.progress_percent.pack(side="right")

        # Modern Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            inner, 
            height=14, 
            corner_radius=7, 
            progress_color=self.colors['success'],
            fg_color=self.colors['console_bg']
        )
        self.progress_bar.pack(fill="x", pady=(0, 15))
        self.progress_bar.set(0)

        # Console Container
        console_container = ctk.CTkFrame(inner, fg_color=self.colors['console_bg'], corner_radius=12, border_width=1, border_color=self.colors['border'])
        console_container.pack(fill="both", expand=True)
        
        # Header for console
        header = ctk.CTkFrame(console_container, fg_color="#1a1a1a", height=32, corner_radius=8)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="  📺 TERMINAL OUTPUT", 
            font=("Consolas", 11, "bold"), 
            text_color="#666666"
        ).pack(side="left", pady=4)
        
        clr_btn = ctk.CTkButton(
            header, text="Clear", command=self.clear_console, 
            width=55, height=22, font=("Segoe UI", 10), 
            fg_color="transparent", hover_color="#333333",
            text_color=self.colors['text_dim']
        )
        clr_btn.pack(side="right", padx=8, pady=4)

        # Standard Text Widget for colored logs
        self.console_text = tk.Text(
            console_container,
            bg=self.colors['console_bg'],
            fg="#e0e0e0",
            font=("Consolas", 10),
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=10,
            wrap="word",
            insertbackground=self.colors['text']
        )
        self.console_text.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))

        con_scroll = ctk.CTkScrollbar(console_container, command=self.console_text.yview)
        con_scroll.pack(side="right", fill="y", padx=8, pady=8)
        self.console_text.config(yscrollcommand=con_scroll.set)

        # Configure Tags for Syntax Highlighting
        self.console_text.tag_configure("success", foreground=self.colors['success'])
        self.console_text.tag_configure("error", foreground=self.colors['error'])
        self.console_text.tag_configure("warning", foreground=self.colors['warning'])
        self.console_text.tag_configure("info", foreground=self.colors['text_dim'])
        self.console_text.tag_configure("accent", foreground=self.colors['accent'])
        self.console_text.tag_configure("header", foreground="#64B5F6", font=("Consolas", 10, "bold"))

        # Intro Log
        self.log_message("🎬 Video Enhancer Pro Initialized\n", "header")
        self.log_message("━" * 50 + "\n", "info")
        self.log_message("AI-powered adaptive video enhancement ready.\n", "info")
        self.log_message("Features: Upscaling • Denoising • Sharpening • Color Correction\n\n", "accent")
        self.log_message("Waiting for input files...\n", "info")

    # --------------------------------------------------------------------------
    # LOGIC METHODS
    # --------------------------------------------------------------------------

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        for f in files:
            if f not in self.files_to_process:
                self.files_to_process.append(f)
                self.file_listbox.insert(tk.END, f" 🎥 {os.path.basename(f)}")
        self.update_file_count()
        if files:
            self.log_message(f"Added {len(files)} file(s)\n", "success")

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
            added = 0
            for file in os.listdir(folder):
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    full_path = os.path.join(folder, file)
                    if full_path not in self.files_to_process:
                        self.files_to_process.append(full_path)
                        self.file_listbox.insert(tk.END, f" 🎥 {file}")
                        added += 1
            if added > 0:
                self.log_message(f"📂 Folder scanned: {folder}\n", "info")
                self.log_message(f"   Found {added} video file(s)\n", "success")
            else:
                self.log_message(f"📂 No video files found in folder\n", "warning")
            self.update_file_count()

    def clear_files(self):
        self.files_to_process.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_file_count()
        self.log_message("🗑️ File list cleared\n", "info")

    def update_file_count(self):
        count = len(self.files_to_process)
        if count == 0:
            text = "No files selected"
        elif count == 1:
            text = "1 file ready"
        else:
            text = f"{count} files ready"
        self.file_count_label.configure(text=text)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_entry.configure(state='normal')
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            self.output_entry.configure(state='disabled')
            self.log_message(f"💾 Output folder set: {folder}\n", "info")

    def reset_output_folder(self):
        self.output_folder = None
        self.output_entry.configure(state='normal')
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, "Same as input folder (default)")
        self.output_entry.configure(state='disabled')
        self.log_message("↺ Output reset to source folder\n", "info")

    def clear_console(self):
        self.console_text.delete(1.0, tk.END)

    def log_message(self, message, tag=None):
        def _log():
            self.console_text.insert(tk.END, message, tag)
            self.console_text.see(tk.END)
        self.after(0, _log)

    def update_progress(self, current, total):
        def _update():
            ratio = current / total if total > 0 else 0
            self.progress_bar.set(ratio)
            self.progress_percent.configure(text=f"{int(ratio * 100)}%")
        self.after(0, _update)

    def update_status(self, text):
        self.after(0, lambda: self.status_label.configure(text=text))

    def get_target_resolution(self):
        """Convert radio button value to resolution tuple"""
        value = self.target_resolution.get()
        if value == "1080p":
            return (1920, 1080)
        elif value == "4k":
            return (3840, 2160)
        elif value == "original":
            return "original"  # Special flag to keep original
        else:  # auto
            return None

    def start_processing(self):
        if not self.files_to_process:
            messagebox.showwarning("No Files", "Please add video files first!")
            return
        
        if self.is_processing:
            return

        self.is_processing = True
        self.start_btn.configure(state='disabled', fg_color="#1a5c40")
        self.stop_btn.configure(state='normal')

        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()

    def stop_processing(self):
        self.is_processing = False
        self.update_status("⏹ Stopping...")
        self.log_message("\n⚠️ [User Abort] Stopping operation...\n", "warning")
        self.start_btn.configure(state='normal', fg_color=self.colors['success'])
        self.stop_btn.configure(state='disabled')

    def process_files(self):
        total_files = len(self.files_to_process)
        successful = 0
        failed = 0
        target_res = self.get_target_resolution()

        self.log_message(f"\n{'═' * 50}\n", "accent")
        self.log_message("🚀 STARTING BATCH VIDEO ENHANCEMENT\n", "header")
        self.log_message(f"{'═' * 50}\n\n", "accent")
        
        resolution_text = "Auto-detect" if target_res is None else ("Original" if target_res == "original" else f"{target_res[0]}x{target_res[1]}")
        self.log_message(f"📐 Target Resolution: {resolution_text}\n", "info")
        self.log_message(f"📁 Processing {total_files} file(s)\n\n", "info")
        
        for i, input_file in enumerate(self.files_to_process):
            if not self.is_processing:
                break
            
            filename = os.path.basename(input_file)
            self.update_status(f"🎥 Processing {i+1}/{total_files}: {filename}")
            self.update_progress(i, total_files)

            self.log_message(f"{'─' * 40}\n", "info")
            self.log_message(f"▶ Processing: {filename}\n", "accent")

            # Determine output file
            if self.output_folder:
                name, ext = os.path.splitext(filename)
                output_file = os.path.join(self.output_folder, f"{name}_enhanced{ext}")
            else:
                output_file = None

            # Capture stdout from VideoEnhancer
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            try:
                # Handle "original" resolution (no upscaling)
                if target_res == "original":
                    enhancer = VideoEnhancer(input_file, output_file=output_file, target_resolution=None)
                    # Override upscaling in enhancement_params after analysis
                else:
                    enhancer = VideoEnhancer(input_file, output_file=output_file, target_resolution=target_res)
                
                if enhancer.process():
                    successful += 1
                    captured = mystdout.getvalue()
                    # Log captured output with proper formatting
                    for line in captured.split('\n'):
                        if line.strip():
                            if '✅' in line or '✨' in line or 'SUCCESS' in line:
                                self.log_message(f"   {line}\n", "success")
                            elif '❌' in line or 'ERROR' in line:
                                self.log_message(f"   {line}\n", "error")
                            elif '⚠️' in line or 'WARNING' in line:
                                self.log_message(f"   {line}\n", "warning")
                            elif '🎯' in line or '📊' in line:
                                self.log_message(f"   {line}\n", "accent")
                            else:
                                self.log_message(f"   {line}\n", "info")
                    self.log_message(f"✅ COMPLETE: {filename}\n", "success")
                else:
                    failed += 1
                    self.log_message(mystdout.getvalue())
                    self.log_message(f"❌ FAILED: {filename}\n", "error")
            except Exception as e:
                failed += 1
                self.log_message(mystdout.getvalue())
                self.log_message(f"❌ EXCEPTION: {str(e)}\n", "error")
            finally:
                sys.stdout = old_stdout

        self.update_progress(total_files, total_files)
        self.log_message(f"\n{'═' * 50}\n", "accent")
        self.log_message("🏁 BATCH ENHANCEMENT COMPLETE\n", "header")
        self.log_message(f"{'═' * 50}\n\n", "accent")
        
        if failed == 0:
            self.log_message(f"✅ All {successful} file(s) enhanced successfully!\n", "success")
        else:
            self.log_message(f"📊 Results: {successful} succeeded, {failed} failed\n", "warning")
        
        self.update_status("✨ Enhancement complete!")
        self.is_processing = False
        
        def _reset_ui():
            self.start_btn.configure(state='normal', fg_color=self.colors['success'])
            self.stop_btn.configure(state='disabled')
            if successful > 0:
                messagebox.showinfo(
                    "Enhancement Complete", 
                    f"Successfully enhanced {successful} video(s).\n\n" + 
                    (f"{failed} file(s) failed." if failed > 0 else "All files processed successfully!")
                )
        
        self.after(0, _reset_ui)


if __name__ == "__main__":
    app = ModernVideoEnhancerGUI()
    app.mainloop()
