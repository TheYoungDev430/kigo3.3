from kigo.qt.backend import QtCore

class DOMBridge(QtCore.QObject):
    nodeSelected = QtCore.Signal(dict)

    @QtCore.Slot(dict)
    def notify(self, data):
        self.nodeSelected.emit(data)