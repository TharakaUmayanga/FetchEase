from yt_dlp import YoutubeDL


class YooutubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def download(self, url):
        with YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])

    def set_video_quality(self, quality):
        video_quality = {
            'best': 'bestvideo+bestaudio/best',
            'high': '137+bestaudio/137/best',
            'medium': '136+bestaudio/136/best',
            'low': '135+bestaudio/135/best',
            'worst': 'worstvideo',
        }
        self.ydl_opts['format'] = video_quality[quality]

    def download_playlist(self, playlist_url, quality='best'):
        # Set format option based on chosen quality
        ydl_opts = {
            'format': self.set_video_quality(quality),  # Fallback to 'best' if quality is not in the dictionary
            'noplaylist': False,  # Ensure downloading entire playlist
            'outtmpl': '%(title)s.%(ext)s'  # Customize output name template (saves as video title)
        }

        # Initialize the downloader with the options
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

    def download_video(self, video_url, quality='best'):
        # Set format option based on chosen quality
        ydl_opts = {
            'format': self.set_video_quality[quality, 'best'],  # Fallback to 'best' if quality is not in the dictionary
            'noplaylist': True,  # Ensures only a single video is downloaded, even if a playlist URL is provided
            'outtmpl': '%(title)s.%(ext)s'  # Customize output name template (saves as video title)
        }

        # Initialize the downloader with the options
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
