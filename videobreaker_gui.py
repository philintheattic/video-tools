import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import sys
from pathlib import Path

class VideoBreakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Breaker - Compression Tool")
        self.root.geometry("600x400")
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.n_iterations = tk.StringVar(value="5")
        self.is_processing = False
        
        # Get FFmpeg path
        self.ffmpeg_path = self.get_ffmpeg_path()
        
        self.setup_ui()
        
    def get_ffmpeg_path(self):
        """Get the path to the FFmpeg executable, whether bundled or system-installed"""
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            application_path = sys._MEIPASS
        else:
            # Running as Python script
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        # Try bundled FFmpeg first
        bundled_ffmpeg = os.path.join(application_path, 'ffmpeg.exe')
        if os.path.exists(bundled_ffmpeg):
            return bundled_ffmpeg
        
        # Fall back to system FFmpeg
        return 'ffmpeg'
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Video Breaker", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Compress your video repeatedly with worst quality settings")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Input Video File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_file, state="readonly")
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse", 
                  command=self.browse_input_file).grid(row=0, column=1)
        
        # Output folder selection
        ttk.Label(main_frame, text="Output Folder:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_folder, state="readonly")
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output_folder).grid(row=0, column=1)
        
        # Number of iterations
        ttk.Label(main_frame, text="Number of Iterations:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        iterations_frame = ttk.Frame(main_frame)
        iterations_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        self.iterations_spinbox = ttk.Spinbox(iterations_frame, from_=1, to=50, width=10,
                                            textvariable=self.n_iterations)
        self.iterations_spinbox.grid(row=0, column=0)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to start...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Processing", 
                                     command=self.start_processing, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                    command=self.stop_processing, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).grid(row=0, column=2, padx=5)
        
        # FFmpeg status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=7, column=0, columnspan=3, pady=(10, 0))
        
        ffmpeg_status = "✓ Bundled FFmpeg detected" if self.ffmpeg_path.endswith('ffmpeg.exe') and os.path.exists(self.ffmpeg_path) else "⚠ Using system FFmpeg"
        ttk.Label(status_frame, text=ffmpeg_status, font=("Arial", 8)).grid(row=0, column=0)
        
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.input_file.set(file_path)
            
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_folder.set(folder_path)
            
    def validate_inputs(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input video file.")
            return False
            
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder.")
            return False
            
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist.")
            return False
            
        if not os.path.exists(self.output_folder.get()):
            messagebox.showerror("Error", "Output folder does not exist.")
            return False
            
        try:
            iterations = int(self.n_iterations.get())
            if iterations < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of iterations must be a positive integer.")
            return False
            
        return True
        
    def start_processing(self):
        if not self.validate_inputs():
            return
            
        self.is_processing = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start processing in a separate thread
        self.processing_thread = threading.Thread(target=self.process_video)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
    def stop_processing(self):
        self.is_processing = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_var.set("Processing stopped by user.")
        
    def process_video(self):
        try:
            input_path = self.input_file.get()
            output_dir = self.output_folder.get()
            n_repeats = int(self.n_iterations.get())
            
            # Get original filename without extension
            original_name = Path(input_path).stem
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Set up progress
            total_steps = n_repeats
            self.progress_bar.config(maximum=total_steps)
            
            # First iteration - compress original file
            if not self.is_processing:
                return
                
            self.progress_var.set("Processing iteration 1...")
            self.root.update()
            
            first_output = os.path.join(output_dir, f"{original_name}_0000.mp4")
            commands_list = [
                self.ffmpeg_path, "-y",  # Use bundled or system FFmpeg
                "-i", input_path,
                "-crf", "63",
                first_output
            ]
            
            result = subprocess.run(commands_list, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
                
            self.progress_bar.config(value=1)
            
            # Subsequent iterations
            for i in range(1, n_repeats):
                if not self.is_processing:
                    return
                    
                self.progress_var.set(f"Processing iteration {i+1}...")
                self.root.update()
                
                input_file = os.path.join(output_dir, f"{original_name}_{i-1:04d}.mp4")
                output_file = os.path.join(output_dir, f"{original_name}_{i:04d}.mp4")
                
                commands_list = [
                    self.ffmpeg_path, "-y",  # Use bundled or system FFmpeg
                    "-i", input_file,
                    "-crf", "63",
                    output_file
                ]
                
                result = subprocess.run(commands_list, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise Exception(f"FFmpeg error: {result.stderr}")
                    
                self.progress_bar.config(value=i+1)
                
            if self.is_processing:
                self.progress_var.set(f"Completed! {n_repeats} iterations processed.")
                messagebox.showinfo("Success", 
                                  f"Video processing completed!\nOutput files saved to: {output_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.progress_var.set("Error occurred during processing.")
            
        finally:
            self.is_processing = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

def main():
    root = tk.Tk()
    app = VideoBreakerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()