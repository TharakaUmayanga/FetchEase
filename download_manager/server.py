import json
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import queue

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension


class DownloadServer:
    def __init__(self, project_root:Path):
        self.app = app
        self.project_root = project_root
        self.config_path = self.project_root / ".config"



        @app.route('/add-download', methods=['POST'])
        def add_download():
            try:
                data = request.json
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



    def run(self, host='localhost', port=5000):
        """Run the server"""
        self.app.run(host=host, port=port)

    def add_pending_downloads(self, download_info:dict):
        """Add download to pending downloads queue"""
        path = self.config_path.joinpath("added_download.json")
        with open(path, "w") as f:
            json.dump(download_info, f)


