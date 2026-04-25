# SPDX-License-Identifier: Zlib
# kigo/debug/freeze.py

from kigo.qt.backend import QtCore, QtWidgets


def freeze(reason: str = "Execution paused", *, data: dict | None = None):
    """
    Freeze execution while keeping the Qt event loop alive.
    Used for visual + state debugging.

    This does NOT crash or block Qt internally.
    """

    # Dialog shown during freeze
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Kigo Time Freeze")
    dialog.setModal(False)
    dialog.setWindowFlags(
        QtCore.Qt.WindowType.WindowStaysOnTopHint
        | QtCore.Qt.WindowType.Dialog
    )

    layout = QtWidgets.QVBoxLayout(dialog)

    label = QtWidgets.QLabel(f"🧊 {reason}")
    label.setStyleSheet("font-weight: bold; font-size: 14px;")
    layout.addWidget(label)

    if data:
        text = QtWidgets.QPlainTextEdit()
        text.setReadOnly(True)
        pretty = "\n".join(f"{k}: {v}" for k, v in data.items())
        text.setPlainText(pretty)
        layout.addWidget(text)

    btn = QtWidgets.QPushButton("Resume")
    layout.addWidget(btn)

    # Local event loop = time freeze
    loop = QtCore.QEventLoop()

    btn.clicked.connect(loop.quit)
    dialog.finished.connect(loop.quit)

    dialog.show()

    # Process paint events before freezing
    QtWidgets.QApplication.processEvents()

    #  TIME FREEZE STARTS HERE
    loop.exec()

    dialog.close()