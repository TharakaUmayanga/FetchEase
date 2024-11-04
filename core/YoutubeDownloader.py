import os
import time

from yt_dlp import YoutubeDL


class YoutubeDownloader:
    def __init__(self, download_path,progress_callback=None ,pause_event=None, stop_event=None):
        self.download_path = download_path
        self.ydl_opts = {}
        self.progress_callback = progress_callback
        self.pause_event = pause_event
        self.stop_event = stop_event

    def _set_video_quality(self, quality):
        video_quality = {
            'best': 'bestvideo+bestaudio/best',
            'high': '137+bestaudio/137/best',
            'medium': '136+bestaudio/136/best',
            'low': '135+bestaudio/135/best',
            'worst': 'worstvideo',
        }
        return video_quality[quality]

    def download_playlist(self, playlist_url, quality='best'):
        extract_opts = {
            'extract_flat': True,  # Extract only metadata, not download
            'playlistend': 1,  # Only need the first item to get the playlist name
            'quiet': True
        }

        with YoutubeDL(extract_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            playlist_title = info.get('title', 'Playlist')

        # Create a directory named after the playlist title
        playlist_folder = os.path.join(self.download_path, playlist_title)
        os.makedirs(playlist_folder, exist_ok=True)
        ydl_opts = {
            'format': self._set_video_quality(quality),
            'noplaylist': False,
            'outtmpl': f'{playlist_folder}/%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook]
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

    def download_video(self, video_url, quality='best'):
        ydl_opts = {
            'format': self._set_video_quality(quality),
            'noplaylist': True,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook]
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def _progress_hook(self, d):
        if self.stop_event and self.stop_event.is_set():
            raise Exception("Download stopped by user")

        if self.pause_event and not self.pause_event.is_set():
            while not self.pause_event.is_set():
                if self.stop_event and self.stop_event.is_set():
                    raise Exception("Download stopped while paused")
                time.sleep(0.1)

        progress_info = {
                'percent': d.get('_percent_str', '0%'),
            'speed': d.get('_speed_str', '0.00KiB/s'),
            'eta': d.get('_eta_str', 'N/A')
            }
        if self.progress_callback:
                self.progress_callback(progress_info)
        elif d['status'] == 'finished':
            print("Download completed! Processing...")

    def download_audio(self, video_url, quality='best'):
        audio_quality = {
            'best': 'bestaudio/best',
            'high': 'bestaudio[abr>128]/best',
            'medium': 'bestaudio[abr<=128]/best',
            'low': 'worstaudio'
        }
        ydl_opts = {
            'format': audio_quality.get(quality, 'bestaudio'),
            'noplaylist': True,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
