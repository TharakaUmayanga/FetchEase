import os
from pathlib import Path
import threading

from download_manager.server import DownloadServer
from ui.MainUI import DownloadManagerGUI

def start_server(server):
    server.run()

if __name__ == '__main__':
    project_root = Path(os.path.dirname(os.path.abspath(__file__)))

    # Initialize server
    server = DownloadServer(project_root)
    # Add routes
    _ = server.add_download_route
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(server,))
    server_thread.daemon = True
    server_thread.start()

    # Initialize and start UI with server instance
    app = DownloadManagerGUI(project_root, server)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()