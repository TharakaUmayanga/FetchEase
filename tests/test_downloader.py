import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
from datetime import datetime

from download_manager.Downloader import Downloader
from download_manager.Settings import Settings

@patch('core.YoutubeDownloader.YoutubeDownloader')
class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.mock_callback = MagicMock()
        with patch('download_manager.Settings.Settings.get_download_path') as mock_path:
            mock_path.return_value = str(Path(__file__).parent / "test_downloads")
            self.downloader = Downloader(ui_callback=self.mock_callback)
        
        # Create test download directories
        os.makedirs(self.downloader.download_path, exist_ok=True)
        os.makedirs(os.path.join(self.downloader.download_path, "video"), exist_ok=True)
        os.makedirs(os.path.join(self.downloader.download_path, "audio"), exist_ok=True)
        os.makedirs(os.path.join(self.downloader.download_path, "playlists"), exist_ok=True)

    def tearDown(self):
        # Clean up test directories
        import shutil
        if os.path.exists(self.downloader.download_path):
            shutil.rmtree(self.downloader.download_path)

    def test_download_video(self, mock_yt):
        test_url = "https://example.com/video"
        test_quality = "best"
        
        mock_instance = mock_yt.return_value
        self.downloader.download_video(test_url, test_quality)
        
        mock_yt.assert_called_once()
        mock_instance.download_video.assert_called_once_with(test_url, test_quality)

    def test_download_audio(self, mock_yt):
        test_url = "https://example.com/video"
        test_quality = "best"
        
        mock_instance = mock_yt.return_value
        self.downloader.download_audio(test_url, test_quality)
        
        mock_yt.assert_called_once()
        mock_instance.download_audio.assert_called_once_with(test_url, test_quality)

    def test_download_queue(self, mock_yt):
        test_queue = [
            {'type': 'video', 'url': 'https://example.com/video1', 'quality': 'best'},
            {'type': 'audio', 'url': 'https://example.com/audio1', 'quality': 'best'},
            {'type': 'playlist', 'url': 'https://example.com/playlist1', 'quality': 'best'}
        ]
        
        with patch.object(self.downloader, 'download_video') as mock_video, \
             patch.object(self.downloader, 'download_audio') as mock_audio, \
             patch.object(self.downloader, 'download_playlist') as mock_playlist:
            
            self.downloader.download_queue(test_queue)
            
            mock_video.assert_called_once_with(test_queue[0]['url'], test_queue[0]['quality'])
            mock_audio.assert_called_once_with(test_queue[1]['url'], test_queue[1]['quality'])
            mock_playlist.assert_called_once_with(test_queue[2]['url'], test_queue[2]['quality'])

    def test_schedule_download(self, mock_yt):
        test_url = "https://example.com/video"
        schedule_time = datetime.now()
        
        with patch.object(self.downloader, 'download_video') as mock_download:
            self.downloader.schedule_download('video', test_url, schedule_time)
            
            # Verify the download was scheduled
            self.assertEqual(len(self.downloader.scheduled_downloads), 1)

    def test_pause_resume(self, mock_yt):
        self.assertTrue(self.downloader.pause_event.is_set())
        
        self.downloader.pause()
        self.assertFalse(self.downloader.pause_event.is_set())
        
        self.downloader.resume()
        self.assertTrue(self.downloader.pause_event.is_set())

    def test_stop(self, mock_yt):
        self.assertFalse(self.downloader.stop_event.is_set())
        
        self.downloader.stop()
        self.assertTrue(self.downloader.stop_event.is_set())

    def test_download_playlist(self, mock_yt):
        test_url = "https://example.com/playlist"
        test_quality = "best"
        
        mock_instance = mock_yt.return_value
        self.downloader.download_playlist(test_url, test_quality)
        
        mock_yt.assert_called_once()
        mock_instance.download_playlist.assert_called_once_with(test_url, test_quality)

if __name__ == '__main__':
    unittest.main()
