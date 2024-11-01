from core.YoutubeDownloader import YoutubeDownloader


class Downloader:
    def __init__(self):
        pass

    def download_queue(self, queue):
        for item in queue:
            if item['type'] == 'video':
                self.download_video(item['url'], item['quality'])
            elif item['type'] == 'playlist':
                self.download_playlist(item['url'], item['quality'])
            elif item['type'] == 'audio':
                self.download_audio(item['url'], item['quality'])
            else:
                print(f"Unknown item type: {item['type']}")

    def download_video(self, url, quality="best"):
        if "youtube.com" in url:
            YoutubeDownloader().download_video(url, quality)
        else:
            Exception("Unsupported website")

    def download_playlist(self, url, quality="best"):
        if "youtube.com" in url:
            YoutubeDownloader().download_playlist(url, quality)
        else:
            Exception("Unsupported website")

    def download_audio(self, url, quality="best"):
        if "youtube.com" in url:
            YoutubeDownloader().download_audio(url, quality)
        else:
            Exception("Unsupported website")
