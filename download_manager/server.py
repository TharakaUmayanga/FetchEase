from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import queue

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension


class DownloadServer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.app = app
        self.pending_downloads = queue.Queue()

        # Start a thread to process pending downloads
        self.process_thread = threading.Thread(target=self._process_pending_downloads)
        self.process_thread.daemon = True
        self.process_thread.start()

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
                self.pending_downloads.put({
                    'url': url,
                    'type': download_type,
                    'quality': quality,
                    'scheduled': is_scheduled,
                    'schedule_time': schedule_time
                })

                return jsonify({
                    'status': 'success',
                    'message': 'Download request received'
                })

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500

    def _process_pending_downloads(self):
        """Process downloads from the queue"""
        while True:
            try:
                # Get next download from queue
                download = self.pending_downloads.get()

                # Schedule GUI update on main thread
                self.main_window.after(0, self._add_download_to_gui, download)

                # Mark task as done
                self.pending_downloads.task_done()

            except Exception as e:
                print(f"Error processing download: {e}")

    def _add_download_to_gui(self, download):
        """Add download to GUI (runs on main thread)"""
        try:
            if download['scheduled']:
                # Handle scheduled download
                schedule_datetime = datetime.fromisoformat(
                    download['schedule_time'].replace('Z', '+00:00')
                )

                # Update date and time pickers in GUI
                self.main_window.date_picker.delete(0, 'end')
                self.main_window.date_picker.insert(0, schedule_datetime.strftime("%Y-%m-%d"))

                self.main_window.time_picker.delete(0, 'end')
                self.main_window.time_picker.insert(0, schedule_datetime.strftime("%H:%M"))

                # Switch to scheduled tab
                self.main_window.tabview.set("Scheduled")

                # Add to scheduled downloads
                self.main_window.schedule_download_from_extension(
                    download['url'],
                    download['type'],
                    download['quality'],
                    schedule_datetime
                )
            else:
                # Set the download type in GUI
                self.main_window.type_var.set(download['type'])

                # Set the quality in GUI
                self.main_window.quality_var.set(download['quality'])

                # Create download item with progress tracking
                item_frame, progress_bar, progress_label = self.main_window.create_download_item(
                    download['url'],
                    download['type']
                )

                # Switch to downloads tab
                self.main_window.tabview.set("Downloads")

                # Start the download with progress tracking
                thread = threading.Thread(
                    target=self.main_window.download_thread,
                    args=(
                        download['url'],
                        download['type'],
                        download['quality'],
                        progress_bar,
                        progress_label
                    )
                )
                thread.daemon = True
                thread.start()

        except Exception as e:
            print(f"Error adding download to GUI: {e}")

    def run(self, host='localhost', port=5000):
        """Run the server"""
        self.app.run(host=host, port=port)
