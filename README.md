# Downloader

An open-source Python project to simplify downloading and managing Video ,Audio and Playlist from Any website. It supports scheduled downloads, queues, and multiple media formats including videos, playlists, and audio.

### Coming Soon
Download any file from any website with ease and convenience.

## Features

- **Download Media**: Supports downloading videos, playlists, and audio in various qualities.
- **Schedule Downloads**: Allows scheduling downloads at specific times with daily recurrence.
- **Queue Management**: Handle multiple downloads sequentially with configurable intervals.

## Download

You can download the pre-built executable for Linux from the releases section.

### Running the Executable

1. Make the file executable:
   ```bash
   chmod +x Downloader
   ```

2. Run the application:
   ```bash
   ./Downloader
   ```

### Building from Source

If you want to build the executable yourself:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Downloader.git
   cd Downloader
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the executable:
   ```bash
   pyinstaller --onefile --windowed --name Downloader --add-data "download_manager:download_manager" --add-data "core:core" main.py
   ```

4. The executable will be created in the `dist` directory.

Note: The executable is platform-specific. You'll need to build it separately for Windows or macOS.

## Use it on your project

## Requirements

- Python 3.7 or later
- Required Python libraries:
  - `schedule`
  - `threading`
  - `datetime`
  - [Additional dependencies as per `core.YoutubeDownloader` and `download_manager.Settings`]

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Downloader.git
   cd Downloader
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure settings in `download_manager.Settings`.

## Usage

### Basic Usage

Import and instantiate the `Downloader` class in your Python project:
```python
from Downloader import Downloader

downloader = Downloader()
downloader.download_video("https://youtube.com/your-video-url", quality="best")
```

### Scheduling Downloads

Schedule a video download for a specific time:
```python
from datetime import datetime

schedule_time = datetime(2024, 11, 25, 15, 30)  # Schedule for Nov 25, 2024, at 3:30 PM
downloader.schedule_download("video", "https://youtube.com/your-video-url", schedule_time)
```

### Managing Download Queue

Create and schedule a download queue:
```python
download_queue = [
    {"type": "video", "url": "https://youtube.com/video1", "quality": "1080p"},
    {"type": "audio", "url": "https://youtube.com/audio1", "quality": "best"},
]

downloader.schedule_download_queue(download_queue, start_time=datetime.now(), interval_minutes=10)
```

## Contributing

We welcome contributions! Please open an issue or submit a pull request with your enhancements or bug fixes.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy downloading!
