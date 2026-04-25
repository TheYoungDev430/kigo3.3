# SPDX-License-Identifier: Zlib
# kigo/inspector/inspector.py

from kigo.qt.backend import QtCore, QtWidgets
from kigo.inspector.overlay import Overlay
from kigo.inspector.panel import InspectorPanel


class Inspector(QtCore.QObject):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()
        self.app = app
        self.overlay = Overlay()
        self.panel = InspectorPanel()

        self.app.installEventFilter(self)

    def attach(self):
        for w in self.app.topLevelWidgets():
            if isinstance(w, QtWidgets.QMainWindow):
                w.addDockWidget(
                    QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
                    self.panel,
                )
                self.overlay.setParent(w)
                self.overlay.resize(w.size())

    def eventFilter(self, obj, event):
        if isinstance(event, QtCore.QEvent):
            if event.type() == QtCore.QEvent.Type.MouseMove:
                widget = self.app.widgetAt(event.globalPosition().toPoint())
                if widget:
                    rect = widget.rect()
                    top_left = widget.mapToGlobal(rect.topLeft())
                    self.overlay.highlight(
                        QtCore.QRect(top_left, rect.size())
                    )

            elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
                widget = self.app.widgetAt(event.globalPosition().toPoint())
                self.panel.inspect(widget)
                return True

        return False


def enable_inspector(app: QtWidgets.QApplication):
    inspector = Inspector(app)
    inspector.attach()
    return inspector