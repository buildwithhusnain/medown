import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import subprocess
import sys

class MediaDownloader:
    def __init__(self, root):
        self.root = root
        self.download_path = os.path.expanduser("~/Downloads")
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Media Downloader")
        self.root.geometry("600x400")
        self.root.configure(bg='black')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='black', foreground='white')
        style.configure('TButton', background='white', foreground='black')
        style.configure('TEntry', fieldbackground='white', foreground='black')
        style.configure('TFrame', background='black')
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Media Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # URL input
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(url_frame, text="Media URL:").pack(anchor='w')
        self.url_entry = ttk.Entry(url_frame, font=('Arial', 10))
        self.url_entry.pack(fill='x', pady=(5, 0))
        
        # Download path
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(path_frame, text="Download Path:").pack(anchor='w')
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill='x', pady=(5, 0))
        
        self.path_entry = ttk.Entry(path_input_frame, font=('Arial', 10))
        self.path_entry.pack(side='left', fill='x', expand=True)
        self.path_entry.insert(0, self.download_path)
        
        browse_btn = ttk.Button(path_input_frame, text="Browse", 
                               command=self.browse_folder)
        browse_btn.pack(side='right', padx=(10, 0))
        
        # Quality selection
        quality_frame = ttk.Frame(main_frame)
        quality_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(quality_frame, text="Quality:").pack(anchor='w')
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                   values=["best", "worst", "720p", "480p", "360p"])
        quality_combo.pack(fill='x', pady=(5, 0))
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download", 
                                      command=self.start_download)
        self.download_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Status text
        self.status_text = tk.Text(main_frame, height=8, bg='black', fg='white',
                                  font=('Consolas', 9))
        self.status_text.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(self.status_text)
        scrollbar.pack(side='right', fill='y')
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    
    def log_message(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        self.download_btn.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.download_media, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_media(self, url):
        try:
            self.log_message(f"Starting download: {url}")
            
            # Base yt-dlp command
            base_cmd = [
                sys.executable, "-m", "yt_dlp",
                "--output", os.path.join(self.download_path, "%(title)s.%(ext)s"),
                "--format", self.get_format_selector(),
                "--no-warnings",
                url
            ]
            
            # Try without proxy first
            self.log_message("Attempting direct download...")
            success = self.run_download(base_cmd)
            
            # If direct download fails, try with proxy
            if not success:
                self.log_message("Direct download failed, trying with proxy...")
                cmd_with_proxy = base_cmd.copy()
                cmd_with_proxy.extend(["--proxy", "socks5://127.0.0.1:9050"])
                success = self.run_download(cmd_with_proxy)
            
            if success:
                self.log_message("Download completed successfully!")
                messagebox.showinfo("Success", "Download completed!")
            else:
                self.log_message("Download failed with all methods!")
                messagebox.showerror("Error", "Download failed!")
                
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Download failed: {str(e)}")
        finally:
            self.progress.stop()
            self.download_btn.config(state='normal')
    
    def run_download(self, cmd):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     universal_newlines=True)
            
            for line in process.stdout:
                if line.strip():
                    self.log_message(line.strip())
            
            process.wait()
            return process.returncode == 0
        except Exception:
            return False
    
    def get_format_selector(self):
        quality = self.quality_var.get()
        if quality == "best":
            return "best[height<=1080]"
        elif quality == "worst":
            return "worst"
        elif quality == "720p":
            return "best[height<=720]"
        elif quality == "480p":
            return "best[height<=480]"
        elif quality == "360p":
            return "best[height<=360]"
        return "best"
    


def main():
    # Check if yt-dlp is installed
    try:
        subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        if messagebox.askyesno("Install yt-dlp", 
                              "yt-dlp is required but not installed. Install it now?"):
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                             check=True)
                messagebox.showinfo("Success", "yt-dlp installed successfully!")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to install yt-dlp")
                return
        else:
            return
    
    root = tk.Tk()
    app = MediaDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()