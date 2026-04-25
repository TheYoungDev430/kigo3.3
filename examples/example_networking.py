from kigo.app import App
from kigo.qt.backend import QtWidgets, QtCore
from kigo.net import req


class NetworkDemo(App):
    def on_start(self):
        # Main window
        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle("Kigo Networking Demo (req)")
        self.win.resize(800, 520)

        # UI
        root = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(root)

        top = QtWidgets.QHBoxLayout()
        self.url = QtWidgets.QLineEdit()
        self.url.setPlaceholderText("https://example.com")
        self.url.setText("https://example.com")
        self.fetch_btn = QtWidgets.QPushButton("Fetch")
        self.fetch_btn.clicked.connect(self.fetch)

        top.addWidget(self.url, 1)
        top.addWidget(self.fetch_btn)

        self.status = QtWidgets.QLabel("Ready.")
        self.status.setStyleSheet("font-weight: bold;")

        self.out = QtWidgets.QPlainTextEdit()
        self.out.setReadOnly(True)

        layout.addLayout(top)
        layout.addWidget(self.status)
        layout.addWidget(self.out, 1)

        self.win.setCentralWidget(root)
        self.win.show()

    def fetch(self):
        url = self.url.text().strip()
        if not url:
            return

        # Basic UX feedback
        self.fetch_btn.setEnabled(False)
        self.status.setText("Fetching…")
        QtWidgets.QApplication.processEvents()

        # Optional: add a simple User-Agent for stricter sites
        headers = {"User-Agent": "KigoNet/1.0 (Qt QNetworkAccessManager)"}

        r = req(url, headers=headers, timeout_ms=15000)

        # Display result
        if r.ok:
            self.status.setText(f"OK {r.status} — {r.url}")
        else:
            self.status.setText(f"ERROR {r.status} — {r.error or 'unknown error'}")

        # Show first part of body to keep UI snappy
        body = r.text
        if len(body) > 20000:
            body = body[:20000] + "\n\n…(truncated)…"

        self.out.setPlainText(body)
        self.fetch_btn.setEnabled(True)


if __name__ == "__main__":
    NetworkDemo(dev=True).run()
