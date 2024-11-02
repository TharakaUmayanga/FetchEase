import os
import time
from datetime import datetime

from core.YoutubeDownloader import YoutubeDownloader
from download_manager.Downloader import Downloader

if __name__ == '__main__':
    downloader = Downloader()

    # Example download queue
    download_queue = [
        {
            'type': 'playlist',
            'url': "https://www.youtube.com/playlist?list=PLPZUrSrcoTOzvCL3_lY8cufqOlF97ZSCx",
            'quality': 'best'
        },
        {
            'type': 'playlist',
            'url': "https://www.youtube.com/playlist?list=PLPZUrSrcoTOzp9n7dQUZ3AXGjSuGexFM5",
            'quality': 'best'
        },
        {
            'type': 'video',
            'url': "https://www.youtube.com/watch?v=-SNSvvyRh4U",
            'quality': 'best'
        },
        {
            'type': 'playlist',
            'url': "https://www.youtube.com/playlist?list=PLPZUrSrcoTOx2m8tzP9hqDAAe-VF9xjqJ",
            'quality': 'best'
        },
    ]


    # Schedule downloads starting from now, with 15-minute intervals
    start_time = datetime(2024, 11, 2, 0, 5)  # Nov 2, 2024 at 10:00 AM

    # Change interval between downloads to 30 minutes
    scheduled_ids = downloader.schedule_download_queue(
        download_queue,
        start_time=start_time,
        interval_minutes=20
    )

    print("\nAll downloads scheduled. Press Ctrl+C to exit.")


    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
