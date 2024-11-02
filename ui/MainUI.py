import customtkinter as ctk
import os
from datetime import datetime
from PIL import Image
import threading
from core.YoutubeDownloader import YoutubeDownloader
from download_manager.Settings import Settings

class DownloadManagerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize settings and downloader
        self.settings = Settings()
        self.download_path = self.settings.get_download_path()
        
        # Configure window
        self.title("FetchEase Download Manager")
        self.geometry("900x600")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize UI elements
        self.setup_ui()
        
        # Store active downloads
        self.active_downloads = []
        self.scheduled_downloads = []

    def setup_ui(self):
        # Create main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Add tabs
        self.tabview.add("Downloads")
        self.tabview.add("Scheduled")
        self.tabview.add("Settings")
        
        self.setup_downloads_tab()
        self.setup_scheduled_tab()
        self.setup_settings_tab()

    def setup_downloads_tab(self):
        downloads_frame = self.tabview.tab("Downloads")
        downloads_frame.grid_columnconfigure(0, weight=1)
        
        # URL input frame
        input_frame = ctk.CTkFrame(downloads_frame)
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        # URL input
        self.url_input = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Enter URL to download...",
            height=40
        )
        self.url_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Control frame (for buttons and dropdowns)
        control_frame = ctk.CTkFrame(downloads_frame)
        control_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        control_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Type selector
        self.type_var = ctk.StringVar(value="video")
        self.type_selector = ctk.CTkSegmentedButton(
            control_frame,
            values=["video", "audio", "playlist"],
            variable=self.type_var
        )
        self.type_selector.grid(row=0, column=0, padx=10, pady=10)
        
        # Quality selector
        self.quality_var = ctk.StringVar(value="best")
        self.quality_selector = ctk.CTkOptionMenu(
            control_frame,
            values=["best", "high", "medium", "low"],
            variable=self.quality_var
        )
        self.quality_selector.grid(row=0, column=1, padx=10, pady=10)
        
        # Download button
        self.download_btn = ctk.CTkButton(
            control_frame,
            text="Download",
            command=self.start_download,
            height=32
        )
        self.download_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Downloads list frame
        downloads_list_frame = ctk.CTkFrame(downloads_frame)
        downloads_list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        downloads_frame.grid_rowconfigure(2, weight=1)
        
        # Downloads scrollable frame
        self.downloads_scroll = ctk.CTkScrollableFrame(downloads_list_frame)
        self.downloads_scroll.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        downloads_list_frame.grid_columnconfigure(0, weight=1)
        downloads_list_frame.grid_rowconfigure(0, weight=1)

    def setup_scheduled_tab(self):
        scheduled_frame = self.tabview.tab("Scheduled")
        scheduled_frame.grid_columnconfigure(0, weight=1)
        
        # Schedule control frame
        schedule_control = ctk.CTkFrame(scheduled_frame)
        schedule_control.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        schedule_control.grid_columnconfigure((0,1), weight=1)
        
        # Date picker
        self.date_picker = ctk.CTkEntry(
            schedule_control,
            placeholder_text="Schedule date (YYYY-MM-DD)"
        )
        self.date_picker.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Time picker
        self.time_picker = ctk.CTkEntry(
            schedule_control,
            placeholder_text="Schedule time (HH:MM)"
        )
        self.time_picker.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Scheduled downloads list
        self.scheduled_scroll = ctk.CTkScrollableFrame(scheduled_frame)
        self.scheduled_scroll.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        scheduled_frame.grid_rowconfigure(1, weight=1)

    def setup_settings_tab(self):
        settings_frame = self.tabview.tab("Settings")
        settings_frame.grid_columnconfigure(0, weight=1)
        
        # Download path frame
        path_frame = ctk.CTkFrame(settings_frame)
        path_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        path_frame.grid_columnconfigure(1, weight=1)
        
        # Path label
        path_label = ctk.CTkLabel(path_frame, text="Download Path:")
        path_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Path input
        self.path_input = ctk.CTkEntry(path_frame)
        self.path_input.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.path_input.insert(0, self.download_path)
        
        # Browse button
        browse_btn = ctk.CTkButton(
            path_frame, 
            text="Browse",
            command=self.browse_path,
            width=100
        )
        browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Save settings button
        save_btn = ctk.CTkButton(
            settings_frame,
            text="Save Settings",
            command=self.save_settings
        )
        save_btn.grid(row=1, column=0, padx=10, pady=10)

    def create_download_item(self, url, download_type):
        """Create a new download item widget"""
        item_frame = ctk.CTkFrame(self.downloads_scroll)
        item_frame.grid(sticky="ew", padx=5, pady=5)
        self.downloads_scroll.grid_columnconfigure(0, weight=1)
        
        # URL label
        url_label = ctk.CTkLabel(
            item_frame,
            text=url[:50] + "..." if len(url) > 50 else url
        )
        url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Type label
        type_label = ctk.CTkLabel(
            item_frame,
            text=download_type.upper(),
            fg_color=("gray70", "gray30"),
            corner_radius=6,
            width=60,
            height=24
        )
        type_label.grid(row=0, column=1, padx=10, pady=5)
        
        # Progress bar
        progress_bar = ctk.CTkProgressBar(item_frame)
        progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,5), sticky="ew")
        progress_bar.set(0)
        
        # Configure grid
        item_frame.grid_columnconfigure(0, weight=1)
        
        return item_frame, progress_bar

    def start_download(self):
        """Start a new download"""
        url = self.url_input.get()
        if not url:
            return
        
        download_type = self.type_var.get()
        quality = self.quality_var.get()
        
        # Create download item in UI
        item_frame, progress_bar = self.create_download_item(url, download_type)
        
        # Start download in separate thread
        thread = threading.Thread(
            target=self.download_thread,
            args=(url, download_type, quality, progress_bar)
        )
        thread.daemon = True
        thread.start()
        
        # Clear URL input
        self.url_input.delete(0, 'end')

    def download_thread(self, url, download_type, quality, progress_bar):
        """Handle download in separate thread"""
        try:
            downloader = YoutubeDownloader(self.download_path)
            
            if download_type == "video":
                downloader.download_video(url, quality)
            elif download_type == "audio":
                downloader.download_audio(url, quality)
            elif download_type == "playlist":
                downloader.download_playlist(url, quality)
            
            # Update progress (you'll need to modify YoutubeDownloader to report progress)
            progress_bar.set(1.0)
            
        except Exception as e:
            print(f"Download error: {e}")
            # Show error in UI
            self.show_error(str(e))

    def schedule_download(self):
        """Schedule a new download"""
        url = self.url_input.get()
        date_str = self.date_picker.get()
        time_str = self.time_picker.get()
        
        try:
            schedule_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            download_type = self.type_var.get()
            quality = self.quality_var.get()
            
            # Add to scheduled downloads
            self.scheduled_downloads.append({
                'url': url,
                'type': download_type,
                'quality': quality,
                'time': schedule_time
            })
            
            # Update scheduled downloads list
            self.update_scheduled_list()
            
            # Clear inputs
            self.url_input.delete(0, 'end')
            self.date_picker.delete(0, 'end')
            self.time_picker.delete(0, 'end')
            
        except ValueError as e:
            self.show_error("Invalid date/time format")

    def browse_path(self):
        """Open directory browser"""
        path = ctk.filedialog.askdirectory()
        if path:
            self.path_input.delete(0, 'end')
            self.path_input.insert(0, path)

    def save_settings(self):
        """Save application settings"""
        new_path = self.path_input.get()
        if os.path.exists(new_path):
            self.download_path = new_path
            self.settings.set_download_path(new_path)
            self.show_success("Settings saved successfully")
        else:
            self.show_error("Invalid download path")

    def show_error(self, message):
        """Show error message"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x150")
        
        label = ctk.CTkLabel(error_window, text=message)
        label.pack(pady=20)
        
        button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        button.pack(pady=10)

    def show_success(self, message):
        """Show success message"""
        success_window = ctk.CTkToplevel(self)
        success_window.title("Success")
        success_window.geometry("300x150")
        
        label = ctk.CTkLabel(success_window, text=message)
        label.pack(pady=20)
        
        button = ctk.CTkButton(
            success_window,
            text="OK",
            command=success_window.destroy
        )
        button.pack(pady=10)

if __name__ == "__main__":
    app = DownloadManagerGUI()
    app.mainloop()