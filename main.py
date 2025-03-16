import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTabWidget, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QByteArray
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest

class GorillaTagBrowser(QMainWindow):
    ICON_URL = "https://kenaccount.netlify.app/icon.ico"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GorillaBrowser")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)

        # Back button
        self.back_button = QPushButton("⏪")
        self.back_button.setToolTip("Navigate back")
        self.back_button.clicked.connect(lambda: self.current_browser().back())
        self.style_button(self.back_button)

        # Forward button
        self.forward_button = QPushButton("⏩")
        self.forward_button.setToolTip("Navigate forward")
        self.forward_button.clicked.connect(lambda: self.current_browser().forward())
        self.style_button(self.forward_button)

        # Reload button
        self.reload_button = QPushButton("🔄")
        self.reload_button.setToolTip("Reload page")
        self.reload_button.clicked.connect(lambda: self.current_browser().reload())
        self.style_button(self.reload_button)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Gorilla Tag mods or enter a URL...")
        self.url_bar.setStyleSheet("""
            padding: 10px;
            border-radius: 15px;
            background-color: #333;
            color: white;
            font-size: 14px;
        """)
        self.url_bar.returnPressed.connect(self.search_gorilla_tag)

        # New tab button
        self.new_tab_button = QPushButton("➕")
        self.new_tab_button.setToolTip("New tab")
        self.new_tab_button.clicked.connect(lambda: self.new_tab("https://gorillastore.netlify.app"))
        self.style_button(self.new_tab_button)

        # Add widgets to navigation layout
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.new_tab_button)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #333;
                color: white;
                padding: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #444;
            }
        """)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Add a default tab
        self.new_tab("https://gorillastore.netlify.app")

        # Add layouts to main layout
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.tabs)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load window icon
        self.load_icon()

    def style_button(self, button):
        """Styles the navigation buttons."""
        button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #444;
                border-radius: 15px;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

    def new_tab(self, url):
        """Creates a new tab with a browser instance."""
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        # Update URL bar when the page changes
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))

    def close_tab(self, index):
        """Closes the tab at the given index."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        """Returns the current browser widget."""
        return self.tabs.currentWidget()

    def search_gorilla_tag(self):
        """Searches for Gorilla Tag mods using the query in the URL bar."""
        query = self.url_bar.text()
        search_url = QUrl(f"https://www.google.com/search?q=Gorilla+Tag+{query}")
        self.current_browser().setUrl(search_url)

    def update_url_bar(self, qurl, browser):
        """Updates the URL bar when the page changes."""
        if browser == self.current_browser():
            self.url_bar.setText(qurl.toString())

    def load_icon(self):
        """Loads the window icon directly from the URL without saving it."""
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.set_icon)
        self.manager.get(QNetworkRequest(QUrl(self.ICON_URL)))

    def set_icon(self, reply):
        """Sets the window icon when the network request completes."""
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(data))
        self.setWindowIcon(QIcon(pixmap))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GorillaTagBrowser()
    window.show()
    sys.exit(app.exec())
