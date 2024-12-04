import json
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import queue

class DownloadServer:
    def __init__(self, project_root:Path):
        self.project_root = project_root
        self.config_path = self.project_root / ".config"
        self.download_callback = None
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for Chrome extension

    def set_download_callback(self, callback):
        """Set callback function to be called when new download is received"""
        self.download_callback = callback

    def add_pending_downloads(self, pending_download):
        """Add download to pending queue and notify UI if callback is set"""
        print(f"Server: Adding pending download: {pending_download}")
        if self.download_callback:
            print("Server: Calling download callback")
            self.download_callback(pending_download)
        else:
            print("Server: Warning - No download callback set")

        path = self.config_path.joinpath("added_download.json")
        print(f"Server: Writing to config file: {path}")
        with open(path, "w") as f:
            json.dump(pending_download, f)

    @property
    def add_download_route(self):
        @self.app.route('/add-download', methods=['POST'])
        def add_download():
            try:
                data = request.json
                print(data)
                url = data['url']
                download_type = data['type']
                quality = data['quality']
                is_scheduled = data['scheduled']
                schedule_time = data.get('scheduleTime')

                # Add to pending downloads queue
                pending_download = {
                    'url': url,
                    'type': download_type,
                    'quality': quality,
                    'scheduled': is_scheduled,
                    'schedule_time': schedule_time
                }
                self.add_pending_downloads(pending_download)

                return jsonify({
                    'status': 'success',
                    'message': 'Download request received'
                })

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500
        return add_download

    def run(self, host='localhost', port=5000):
        """Run the server"""
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    server = DownloadServer(Path('.'))
    server.add_download_route
    server.run()
