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
        self.setStyleSheet("background-color: #222; color: white;")

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet("QTabBar::tab { background: black; color: white; padding: 10px; } QTabBar::tab:selected { background: #444; }")
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.new_tab("https://www.genesis.menu")

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Gorilla Tag mods...")
        self.url_bar.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #333; color: white;")
        self.url_bar.returnPressed.connect(self.search_gorilla_tag)
        
        self.back_button = QPushButton("⏪")
        self.back_button.setStyleSheet("padding: 10px; background-color: #444; border-radius: 5px; color: white;")
        self.back_button.clicked.connect(lambda: self.current_browser().back())
        
        self.forward_button = QPushButton("⏩")
        self.forward_button.setStyleSheet("padding: 10px; background-color: #444; border-radius: 5px; color: white;")
        self.forward_button.clicked.connect(lambda: self.current_browser().forward())
        
        self.reload_button = QPushButton("🔄")
        self.reload_button.setStyleSheet("padding: 10px; background-color: #444; border-radius: 5px; color: white;")
        self.reload_button.clicked.connect(lambda: self.current_browser().reload())
        
        self.new_tab_button = QPushButton("➕")
        self.new_tab_button.setStyleSheet("padding: 10px; background-color: #444; border-radius: 5px; color: white;")
        self.new_tab_button.clicked.connect(lambda: self.new_tab("https://www.google.com"))
        
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.new_tab_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.tabs)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.load_icon()

    def new_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        return self.tabs.currentWidget()

    def search_gorilla_tag(self):
        query = self.url_bar.text()
        search_url = QUrl(f"https://www.google.com/search?q=Gorilla+Tag+{query}")
        self.current_browser().setUrl(search_url)

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
