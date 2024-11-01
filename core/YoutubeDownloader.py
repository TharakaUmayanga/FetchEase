from yt_dlp import YoutubeDL

class YoutubeDownloader:
    def __init__(self, download_path):
        self.download_path = download_path
        self.ydl_opts = {}

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
        ydl_opts = {
            'format': self._set_video_quality(quality),
            'noplaylist': False,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
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
        if d['status'] == 'downloading':
            print(f"Downloading: {d['_percent_str']} at {d['_speed_str']} - ETA: {d['_eta_str']}")
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