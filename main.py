import os
from pathlib import Path
import threading

from download_manager.server import DownloadServer
from ui.MainUI import DownloadManagerGUI

def start_server(project_root):
    server = DownloadServer(project_root)
    server.run()

if __name__ == '__main__':
    project_root = Path(os.path.dirname(os.path.abspath(__file__)))

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(project_root,))
    server_thread.daemon = True
    server_thread.start()

    app = DownloadManagerGUI(project_root)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()