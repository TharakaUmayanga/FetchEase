# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

class DownloadServer:
    def __init__(self, download_manager):
        self.download_manager = download_manager
        self.app = app

        @app.route('/add-download', methods=['POST'])
        def add_download():
            try:
                data = request.json
                url = data['url']
                download_type = data['type']
                quality = data['quality']
                is_scheduled = data['scheduled']
                schedule_time = data.get('scheduleTime')

                if is_scheduled and schedule_time:
                    # Convert schedule_time string to datetime object
                    schedule_datetime = datetime.fromisoformat(schedule_time.replace('Z', '+00:00'))
                    # Schedule the download
                    download_id = self.download_manager.schedule_download(
                        download_type,
                        url,
                        schedule_datetime,
                        quality
                    )
                    return jsonify({'status': 'success', 'message': 'Download scheduled', 'id': download_id})
                else:
                    # Start immediate download
                    thread = threading.Thread(
                        target=self.start_download,
                        args=(url, download_type, quality)
                    )
                    thread.daemon = True
                    thread.start()
                    return jsonify({'status': 'success', 'message': 'Download started'})

            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500

    def start_download(self, url, download_type, quality):
        """Start a download based on type"""
        try:
            if download_type == "video":
                self.download_manager.download_video(url, quality)
            elif download_type == "audio":
                self.download_manager.download_audio(url, quality)
            elif download_type == "playlist":
                self.download_manager.download_playlist(url, quality)
        except Exception as e:
            print(f"Download error: {e}")

    def run(self, host='localhost', port=5000):
        """Run the server"""
        self.app.run(host=host, port=port)