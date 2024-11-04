import os
import threading
from datetime import datetime, timedelta

import schedule
import time
from core.YoutubeDownloader import YoutubeDownloader
from download_manager.Settings import Settings


class Downloader:
    def __init__(self,ui_callback=None):
        self.download_path = Settings().get_download_path()
        self.scheduled_downloads = []
        self.ui_callback = ui_callback

        self._start_scheduler_thread()
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()
        self.pause_event.set()

    def _progress_callback(self, progress_info, progress_bar, progress_label):
        if self.ui_callback:
            self.ui_callback(progress_info, progress_bar, progress_label)

    def _start_scheduler_thread(self):
        """
        Start a background thread to run the scheduler.
        This ensures scheduled downloads can occur without blocking the main thread.
        """
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()


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

    def download_video(self, url, quality="best",progress_bar=None, progress_label=None):
        download_path = os.path.join(self.download_path, "video")
        # if "youtube.com" in url:
        YoutubeDownloader(download_path,lambda info: self._progress_callback(info, progress_bar, progress_label), self.pause_event, self.stop_event).download_video(url, quality)
        # else:
        #     Exception("Unsupported website")

    def download_playlist(self, url, quality="best",progress_bar=None, progress_label=None):
        download_path = os.path.join(self.download_path, "playlists")
        if "youtube.com" in url:
            YoutubeDownloader(download_path,lambda info: self._progress_callback(info, progress_bar, progress_label), self.pause_event, self.stop_event).download_path(url, quality)
        else:
            Exception("Unsupported website")

    def download_audio(self, url, quality="best",progress_bar=None, progress_label=None):
        download_path = os.path.join(self.download_path, "audio")
        if "youtube.com" in url:
            YoutubeDownloader(download_path,lambda info: self._progress_callback(info, progress_bar, progress_label), self.pause_event, self.stop_event).download_audio(url, quality)
        else:
            Exception("Unsupported website")


    def schedule_download(self, download_type, url, schedule_time, quality="best"):
        """
        Schedule a download at a specific time.

        :param download_type: 'video', 'playlist', or 'audio'
        :param url: URL to download
        :param schedule_time: Time to schedule the download (datetime object)
        :param quality: Download quality (default is 'best')
        :return: Scheduled download ID
        """
        def scheduled_download():
            try:
                if download_type == 'video':
                    self.download_video(url, quality)
                elif download_type == 'playlist':
                    self.download_playlist(url, quality)
                elif download_type == 'audio':
                    self.download_audio(url, quality)
                else:
                    print(f"Unknown download type: {download_type}")

                # Remove this scheduled download after execution
                self._remove_scheduled_download(scheduled_download)
            except Exception as e:
                print(f"Scheduled download failed: {e}")

        # Convert datetime to time string
        time_str = schedule_time.strftime("%H:%M")

        # Schedule the job
        job = schedule.every().day.at(time_str).do(scheduled_download)

        # Store download details for tracking
        download_info = {
            'id': id(scheduled_download),
            'type': download_type,
            'url': url,
            'quality': quality,
            'scheduled_time': schedule_time,
            'job': job
        }
        self.scheduled_downloads.append(download_info)

        return download_info['id']

    def cancel_scheduled_download(self, download_id):
        """
        Cancel a scheduled download by its ID.

        :param download_id: ID of the scheduled download to cancel
        """
        for download in self.scheduled_downloads[:]:
            if download['id'] == download_id:
                schedule.cancel_job(download['job'])
                self.scheduled_downloads.remove(download)
                print(f"Cancelled scheduled download for {download['url']}")
                return True

        print(f"No scheduled download found with ID {download_id}")
        return False

    def _remove_scheduled_download(self, scheduled_func):
        """
        Internal method to remove a scheduled download after execution.

        :param scheduled_func: The scheduled function to remove
        """
        self.scheduled_downloads = [
            download for download in self.scheduled_downloads
            if id(scheduled_func) != download['id']
        ]

    def list_scheduled_downloads(self):
        """
        List all currently scheduled downloads.

        :return: List of scheduled download details
        """
        return [
            {
                'id': download['id'],
                'type': download['type'],
                'url': download['url'],
                'quality': download['quality'],
                'scheduled_time': download['scheduled_time']
            }
            for download in self.scheduled_downloads
        ]

    def schedule_download_queue(self, download_queue, start_time=None, interval_minutes=15):
        """
        Schedule multiple downloads in sequence.

        :param download_queue: List of download items
            Each item is a dict with keys:
            - 'type': 'video', 'playlist', or 'audio'
            - 'url': URL to download
            - 'quality': Optional download quality (default 'best')
        :param start_time: Datetime to start the first download (default is now)
        :param interval_minutes: Minutes between each download
        :return: List of scheduled download IDs
        """
        # If no start time is provided, use current time
        current_time = start_time or datetime.now()

        # List to store scheduled download IDs
        scheduled_ids = []

        # Queue downloads with increasing time intervals
        for index, item in enumerate(download_queue):
            # Calculate scheduled time for each download
            download_time = current_time + timedelta(minutes=index * interval_minutes)

            # Schedule the download
            scheduled_id = self.schedule_download(
                item['type'],
                item['url'],
                download_time,
                item.get('quality', 'best')
            )

            scheduled_ids.append(scheduled_id)

            # Print scheduled download details
            print(f"Scheduled {item['type']} download {index + 1}: ")
            print(f"  URL: {item['url']}")
            print(f"  Time: {download_time}")
            print(f"  Scheduled ID: {scheduled_id}")
            print("---")

        return scheduled_ids

    def pause_download(self):
        self.pause_event.clear()

    def resume_download(self):
        self.pause_event.set()

    def stop_download(self):
        self.stop_event.set()
        # Reset stop event for future downloads
        threading.Timer(1.0, self.stop_event.clear).start()


