"""
🎵 Professional Audio Cleaner GUI
A beautiful, modern interface for the Adaptive Audio Cleaner
Uses the same AI-powered adaptive processing

DEPENDENCY: pip install customtkinter
"""

import os
import sys
import threading
from io import StringIO
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Import the cleaner logic
try:
    from .core import AudioCleaner
except ImportError:
    from core import AudioCleaner

# --- THEME CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernAudioCleanerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Audio Cleaner Pro AI")
        self.geometry("1000x800")
        self.minsize(900, 700)
        
        # Color Palette (Dark Modern)
        self.colors = {
            'bg': '#1a1a1a',           # Main Window BG
            'card': '#2b2b2b',         # Card/Section BG
            'accent': '#3B8ED0',       # Primary Blue
            'success': '#2CC985',      # Success Green
            'error': '#E53935',        # Error Red
            'text': '#E0E0E0',         # Primary Text
            'text_dim': '#A0A0A0',     # Secondary Text
            'console_bg': '#1e1e1e'    # Console specific dark
        }

        # Variables
        self.files_to_process = []
        self.output_folder = None
        self.is_processing = False

        # Build UI
        self.create_ui()

    def create_ui(self):
        """Create the modern card-based UI"""
        # Main container with padding
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. Header Section
        self.create_header(main_frame)

        # 2. Workspace Area (Split layout optional, using Stack for simplicity)
        workspace = ctk.CTkFrame(main_frame, fg_color="transparent")
        workspace.pack(fill="both", expand=True)

        # Files Card
        self.create_file_section(workspace)
        
        # Settings & Actions Container (Horizontal layout)
        controls_row = ctk.CTkFrame(workspace, fg_color="transparent")
        controls_row.pack(fill="x", pady=(0, 15))
        
        # Output Folder (Left side of controls)
        self.create_output_section(controls_row)
        
        # Start/Stop Actions (Right side of controls)
        self.create_action_section(controls_row)

        # Progress & Console Card
        self.create_console_section(workspace)

    def create_header(self, parent):
        """Header with modern typography"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        # Icon & Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎵 Audio Cleaner Pro", 
            font=("Roboto Medium", 32),
            text_color=self.colors['text']
        )
        title_label.pack(side="left")

        # Subtitle / AI Badge
        badge = ctk.CTkLabel(
            header_frame,
            text=" AI POWERED ",
            font=("Roboto", 10, "bold"),
            fg_color=self.colors['accent'],
            text_color="white",
            corner_radius=6,
            height=24
        )
        badge.pack(side="left", padx=15, pady=5)

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Adaptive Noise Reduction & Enhancement",
            font=("Roboto", 12),
            text_color=self.colors['text_dim']
        )
        subtitle.pack(side="left", padx=0)

    def create_file_section(self, parent):
        """File selection card"""
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Inner padding frame
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=15, fill="x")

        # Title Row
        top_row = ctk.CTkFrame(inner, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            top_row, 
            text="INPUT FILES", 
            font=("Roboto", 14, "bold"), 
            text_color=self.colors['text']
        ).pack(side="left")

        self.file_count_label = ctk.CTkLabel(
            top_row, 
            text="0 files selected", 
            font=("Roboto", 12), 
            text_color=self.colors['text_dim']
        )
        self.file_count_label.pack(side="right")

        # Layout: Listbox on left, Buttons on right
        content_row = ctk.CTkFrame(inner, fg_color="transparent")
        content_row.pack(fill="x")

        # Custom Listbox Container (Using standard tk.Listbox for logic compatibility but styled)
        list_container = ctk.CTkFrame(content_row, fg_color=self.colors['console_bg'], corner_radius=10, border_width=1, border_color="#404040")
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
            font=("Consolas", 11)
        )
        self.file_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Scrollbar for listbox
        scrollbar = ctk.CTkScrollbar(list_container, command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y", padx=(0,5), pady=5)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons Column
        btn_col = ctk.CTkFrame(content_row, fg_color="transparent")
        btn_col.pack(side="right", padx=(15, 0), fill="y")

        self.add_files_btn = ctk.CTkButton(
            btn_col, text="Add Files", command=self.add_files, 
            width=120, height=35, fg_color=self.colors['accent']
        )
        self.add_files_btn.pack(pady=(0, 8))

        self.add_folder_btn = ctk.CTkButton(
            btn_col, text="Add Folder", command=self.add_folder, 
            width=120, height=35, fg_color="transparent", border_width=1, border_color=self.colors['accent']
        )
        self.add_folder_btn.pack(pady=(0, 8))

        self.clear_btn = ctk.CTkButton(
            btn_col, text="Clear All", command=self.clear_files, 
            width=120, height=35, fg_color="transparent", text_color=self.colors['error'], hover_color="#331010"
        )
        self.clear_btn.pack(side="bottom")

    def create_output_section(self, parent):
        """Output folder selection"""
        # We put this in a frame that only takes up needed space
        container = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=15)
        container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both")

        ctk.CTkLabel(inner, text="OUTPUT DESTINATION", font=("Roboto", 12, "bold"), text_color=self.colors['text_dim']).pack(anchor="w", pady=(0, 8))

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x")

        self.output_entry = ctk.CTkEntry(row, placeholder_text="Default: Same as input", height=35, border_color="#404040")
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.output_entry.insert(0, "Same as input folder (default)")
        self.output_entry.configure(state="disabled")

        ctk.CTkButton(row, text="Browse", width=80, height=35, command=self.select_output_folder).pack(side="left", padx=(0, 5))
        ctk.CTkButton(row, text="↺", width=35, height=35, command=self.reset_output_folder, fg_color="#404040").pack(side="left")

    def create_action_section(self, parent):
        """Start button and simple controls"""
        container = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=15)
        container.pack(side="right", fill="both") # Fixed width for action button area

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both", expand=True)

        self.start_btn = ctk.CTkButton(
            inner, 
            text="START PROCESSING", 
            font=("Roboto", 15, "bold"),
            command=self.start_processing,
            fg_color=self.colors['success'],
            hover_color="#26a870",
            height=50,
            width=200
        )
        self.start_btn.pack(side="left", padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            inner,
            text="STOP",
            font=("Roboto", 12, "bold"),
            command=self.stop_processing,
            fg_color=self.colors['error'],
            hover_color="#b02622",
            height=50,
            width=60,
            state="disabled"
        )
        self.stop_btn.pack(side="right")

    def create_console_section(self, parent):
        """Logs and Progress"""
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=15)
        card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both", expand=True)

        # Status Bar
        status_row = ctk.CTkFrame(inner, fg_color="transparent")
        status_row.pack(fill="x", pady=(0, 10))

        self.status_label = ctk.CTkLabel(status_row, text="Ready to clean audio", font=("Roboto", 12), text_color=self.colors['text'])
        self.status_label.pack(side="left")

        self.progress_percent = ctk.CTkLabel(status_row, text="0%", font=("Roboto", 12, "bold"), text_color=self.colors['accent'])
        self.progress_percent.pack(side="right")

        # Modern Progress Bar
        self.progress_bar = ctk.CTkProgressBar(inner, height=12, corner_radius=6, progress_color=self.colors['success'])
        self.progress_bar.pack(fill="x", pady=(0, 15))
        self.progress_bar.set(0)

        # Console Container
        console_container = ctk.CTkFrame(inner, fg_color=self.colors['console_bg'], corner_radius=10, border_width=1, border_color="#404040")
        console_container.pack(fill="both", expand=True)
        
        # Header for console
        header = ctk.CTkFrame(console_container, fg_color="#252525", height=30, corner_radius=6)
        header.pack(fill="x", padx=1, pady=1)
        ctk.CTkLabel(header, text="  TERMINAL OUTPUT", font=("Consolas", 10, "bold"), text_color="#666").pack(side="left")
        
        clr_btn = ctk.CTkButton(header, text="Clear", command=self.clear_console, width=50, height=20, font=("Roboto", 10), fg_color="transparent", hover_color="#333")
        clr_btn.pack(side="right", padx=5)

        # Standard Text Widget for colored logs (integrated into CTk Frame)
        self.console_text = tk.Text(
            console_container,
            bg=self.colors['console_bg'],
            fg="#d0d0d0",
            font=("Consolas", 10),
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            wrap="word"
        )
        self.console_text.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)

        con_scroll = ctk.CTkScrollbar(console_container, command=self.console_text.yview)
        con_scroll.pack(side="right", fill="y", padx=5, pady=5)
        self.console_text.config(yscrollcommand=con_scroll.set)

        # Configure Tags for Syntax Highlighting
        self.console_text.tag_configure("success", foreground=self.colors['success'])
        self.console_text.tag_configure("error", foreground=self.colors['error'])
        self.console_text.tag_configure("warning", foreground="#FFB300")
        self.console_text.tag_configure("info", foreground=self.colors['text_dim'])
        self.console_text.tag_configure("accent", foreground=self.colors['accent'])

        # Intro Log
        self.log_message("System initialized. AI Audio Cleaner ready.\n", "info")
        self.log_message("Waiting for input files...\n", "accent")

    # --------------------------------------------------------------------------
    # LOGIC METHODS (Preserved functionality with minimal UI updates)
    # --------------------------------------------------------------------------

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[("Audio files", "*.wav *.mp3 *.m4a *.flac *.aac *.ogg"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.files_to_process:
                self.files_to_process.append(f)
                self.file_listbox.insert(tk.END, f" {os.path.basename(f)}")
        self.update_file_count()

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg']
            added = 0
            for file in os.listdir(folder):
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    full_path = os.path.join(folder, file)
                    if full_path not in self.files_to_process:
                        self.files_to_process.append(full_path)
                        self.file_listbox.insert(tk.END, f" {file}")
                        added += 1
            if added > 0:
                self.log_message(f"Folder added: {folder} ({added} files)\n", "info")
            self.update_file_count()

    def clear_files(self):
        self.files_to_process.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_file_count()
        self.log_message("File list cleared.\n", "info")

    def update_file_count(self):
        count = len(self.files_to_process)
        text = "No files selected" if count == 0 else f"{count} files ready"
        self.file_count_label.configure(text=text)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_entry.configure(state='normal')
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            self.output_entry.configure(state='disabled')
            self.log_message(f"Output set to: {folder}\n", "info")

    def reset_output_folder(self):
        self.output_folder = None
        self.output_entry.configure(state='normal')
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, "Same as input folder (default)")
        self.output_entry.configure(state='disabled')
        self.log_message("Output reset to source folder.\n", "info")

    def clear_console(self):
        self.console_text.delete(1.0, tk.END)

    def log_message(self, message, tag=None):
        def _log():
            self.console_text.insert(tk.END, message, tag)
            self.console_text.see(tk.END)
        self.after(0, _log)

    def update_progress(self, current, total):
        def _update():
            # CTkProgressBar takes float 0.0 to 1.0
            ratio = current / total if total > 0 else 0
            self.progress_bar.set(ratio)
            self.progress_percent.configure(text=f"{int(ratio * 100)}%")
        self.after(0, _update)

    def update_status(self, text):
        self.after(0, lambda: self.status_label.configure(text=text))

    def start_processing(self):
        if not self.files_to_process:
            messagebox.showwarning("No Files", "Please add audio files first!")
            return
        
        if self.is_processing:
            return

        self.is_processing = True
        self.start_btn.configure(state='disabled', fg_color="#1a5c40") # Darker green when disabled
        self.stop_btn.configure(state='normal')

        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()

    def stop_processing(self):
        self.is_processing = False
        self.update_status("Stopping...")
        self.log_message("\n[User Abort] Stopping operation...\n", "warning")
        self.start_btn.configure(state='normal', fg_color=self.colors['success'])
        self.stop_btn.configure(state='disabled')

    def process_files(self):
        total_files = len(self.files_to_process)
        successful = 0
        failed = 0

        self.log_message(f"\n{'='*40}\nSTARTING BATCH PROCESS\n{'='*40}\n", "accent")
        
        for i, input_file in enumerate(self.files_to_process):
            if not self.is_processing:
                break
            
            filename = os.path.basename(input_file)
            self.update_status(f"Processing {i+1}/{total_files}: {filename}")
            self.update_progress(i, total_files)

            self.log_message(f"--> Processing: {filename}\n", "info")

            if self.output_folder:
                name, _ = os.path.splitext(filename)
                output_file = os.path.join(self.output_folder, f"{name}_cleaned.wav")
            else:
                output_file = None

            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            try:
                cleaner = AudioCleaner(input_file, output_file=output_file, target_sample_rate=48000)
                if cleaner.process():
                    saved_file = cleaner.save_audio(format='WAV')
                    if saved_file:
                        successful += 1
                        captured = mystdout.getvalue()
                        self.log_message(captured)
                        self.log_message(f"    COMPLETE: Saved to {os.path.basename(saved_file)}\n", "success")
                    else:
                        failed += 1
                        self.log_message(mystdout.getvalue())
                        self.log_message(f"    ERROR: Could not save file.\n", "error")
                else:
                    failed += 1
                    self.log_message(mystdout.getvalue())
                    self.log_message(f"    ERROR: Processing failed.\n", "error")
            except Exception as e:
                failed += 1
                self.log_message(mystdout.getvalue())
                self.log_message(f"    EXCEPTION: {str(e)}\n", "error")
            finally:
                sys.stdout = old_stdout

        self.update_progress(total_files, total_files)
        self.log_message(f"\n{'='*40}\nBATCH COMPLETE\n{'='*40}\n", "accent")
        self.log_message(f"Success: {successful} | Failed: {failed}\n\n", "success" if failed == 0 else "warning")
        
        self.update_status("Processing finished")
        self.is_processing = False
        
        def _reset_ui():
            self.start_btn.configure(state='normal', fg_color=self.colors['success'])
            self.stop_btn.configure(state='disabled')
            if successful > 0:
                messagebox.showinfo("Done", f"Processed {successful} files successfully.")
        
        self.after(0, _reset_ui)

if __name__ == "__main__":
    app = ModernAudioCleanerGUI()
    app.mainloop()