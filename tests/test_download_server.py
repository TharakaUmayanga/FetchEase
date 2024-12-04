import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from download_manager.server import DownloadServer

class TestDownloadServer(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent / "test_data"
        self.test_dir.mkdir(exist_ok=True)
        self.config_dir = self.test_dir / ".config"
        self.config_dir.mkdir(exist_ok=True)
        self.server = DownloadServer(self.test_dir)
        # Register routes
        _ = self.server.add_download_route
        
    def tearDown(self):
        # Clean up test files
        for file in self.config_dir.glob("*"):
            file.unlink()
        self.config_dir.rmdir()
        self.test_dir.rmdir()

    def test_set_download_callback(self):
        mock_callback = MagicMock()
        self.server.set_download_callback(mock_callback)
        self.assertEqual(self.server.download_callback, mock_callback)

    def test_add_pending_downloads(self):
        mock_callback = MagicMock()
        self.server.set_download_callback(mock_callback)
        
        test_download = {
            'url': 'https://test.com/video',
            'type': 'video',
            'quality': 'best',
            'scheduled': False,
            'schedule_time': None
        }
        
        self.server.add_pending_downloads(test_download)
        
        # Verify callback was called
        mock_callback.assert_called_once_with(test_download)
        
        # Verify file was written
        config_file = self.config_dir / "added_download.json"
        self.assertTrue(config_file.exists())
        
        with open(config_file) as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, test_download)

    def test_add_download_route(self):
        test_client = self.server.app.test_client()
        
        test_data = {
            'url': 'https://test.com/video',
            'type': 'video',
            'quality': 'best',
            'scheduled': False,
            'scheduleTime': None
        }
        
        response = test_client.post('/add-download', 
                                  json=test_data,
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        
        # Verify file was written
        config_file = self.config_dir / "added_download.json"
        self.assertTrue(config_file.exists())
        
        with open(config_file) as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data['url'], test_data['url'])
        self.assertEqual(saved_data['type'], test_data['type'])

    def test_add_download_route_error(self):
        test_client = self.server.app.test_client()
        
        # Missing required fields
        test_data = {
            'url': 'https://test.com/video'
        }
        
        response = test_client.post('/add-download', 
                                  json=test_data,
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'error')

if __name__ == '__main__':
    unittest.main()
