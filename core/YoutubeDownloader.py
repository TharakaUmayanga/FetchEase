from yt_dlp import YoutubeDL


class YoutubeDownloader:
    def __init__(self):
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
        # Set format option based on chosen quality
        ydl_opts = {
            'format': self._set_video_quality(quality),  # Fallback to 'best' if quality is not in the dictionary
            'noplaylist': False,  # Ensure downloading entire playlist
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook]
        }

        # Initialize the downloader with the options
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])


    def download_video(self, video_url, quality='best'):
        # Set format option based on chosen quality
        ydl_opts = {
            'format': self._set_video_quality(quality),
            # Fallback to 'best' if quality is not in the dictionary
            'noplaylist': True,  # Ensures only a single video is downloaded, even if a playlist URL is provided
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook]
        }

        # Initialize the downloader with the options
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            print(f"Downloading: {d['_percent_str']} at {d['_speed_str']} - ETA: {d['_eta_str']}")
        elif d['status'] == 'finished':
            print("Download completed! Processing...")

    def download_audio(self, video_url, quality='best'):
        # Set format option to audio only based on chosen quality
        audio_quality = {
            'best': 'bestaudio/best',
            'high': 'bestaudio[abr>128]/best',  # Audio bitrate > 128 kbps
            'medium': 'bestaudio[abr<=128]/best',  # Audio bitrate <= 128 kbps
            'low': 'worstaudio'
        }
        ydl_opts = {
            'format': audio_quality.get(quality, 'bestaudio'),
            # Fallback to 'bestaudio' if quality not in the dictionary
            'noplaylist': True,  # Ensures only a single video is processed
            'outtmpl': '%(title)s.%(ext)s',  # Customize output file name using video title
            'progress_hooks': [self._progress_hook],  # Add the progress hook function
            'postprocessors': [{  # Convert audio to mp3 format after download
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Set bitrate for mp3
            }],
        }

        # Initialize the downloader with the options
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
