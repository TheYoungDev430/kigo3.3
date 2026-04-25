from kigo.qt.backend import QtCore

# Alias Signal correctly for PyQt6 and PySide6
Signal = getattr(QtCore, "Signal", QtCore.pyqtSignal)


class AndroidLifecycle(QtCore.QObject):
    paused = Signal()
    resumed = Signal()

    def __init__(self, app):
        super().__init__()
        self.app = app
        app.applicationStateChanged.connect(self._on_state)

    def _on_state(self, state):
        if state == QtCore.Qt.ApplicationState.ApplicationSuspended:
            self.paused.emit()
        elif state == QtCore.Qt.ApplicationState.ApplicationActive:
            self.resumed.emit()
