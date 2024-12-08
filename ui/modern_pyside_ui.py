import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QLabel,
                             QScrollArea, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPalette, QColor

class ModernWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FetchEase")
        self.setMinimumSize(900, 600)
        
        # Set the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton#secondary {
                background-color: #9E9E9E;
            }
            QPushButton#secondary:hover {
                background-color: #757575;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QLabel#title {
                color: #1565C0;
                font-size: 24px;
                font-weight: bold;
            }
            QFrame#card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        # Header
        header = QHBoxLayout()
        title = QLabel("FetchEase")
        title.setObjectName("title")
        header.addWidget(title)
        header.addStretch()
        
        settings_btn = QPushButton("Settings")
        settings_btn.setFixedWidth(100)
        header.addWidget(settings_btn)
        layout.addLayout(header)

        # Search section
        search_container = QFrame()
        search_container.setObjectName("card")
        search_layout = QVBoxLayout(search_container)
        
        search_label = QLabel("Search")
        search_label.setFont(QFont("Arial", 12))
        search_layout.addWidget(search_label)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter your search query...")
        search_layout.addWidget(search_input)
        
        button_layout = QHBoxLayout()
        search_btn = QPushButton("Search")
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondary")
        button_layout.addWidget(search_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        search_layout.addLayout(button_layout)
        
        layout.addWidget(search_container)

        # Content area
        content_container = QFrame()
        content_container.setObjectName("card")
        content_container.setMinimumHeight(300)
        content_layout = QVBoxLayout(content_container)
        
        content_label = QLabel("Results")
        content_label.setFont(QFont("Arial", 12))
        content_layout.addWidget(content_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Add some placeholder content
        for i in range(5):
            item = QFrame()
            item.setObjectName("card")
            item_layout = QVBoxLayout(item)
            item_layout.addWidget(QLabel(f"Result Item {i+1}"))
            scroll_layout.addWidget(item)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        content_layout.addWidget(scroll_area)
        
        layout.addWidget(content_container)

        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("background-color: white; padding: 5px;")

def main():
    app = QApplication(sys.argv)
    window = ModernWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
