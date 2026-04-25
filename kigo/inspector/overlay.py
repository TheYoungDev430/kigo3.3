# SPDX-License-Identifier: Zlib
# kigo/inspector/overlay.py

from kigo.qt.backend import QtWidgets, QtGui, QtCore


class Overlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        self.hide()

        self._rect = None

    def highlight(self, rect: QtCore.QRect):
        self._rect = rect
        self.setGeometry(rect.adjusted(-2, -2, 2, 2))
        self.show()
        self.raise_()
        self.update()

    def clear(self):
        self._rect = None
        self.hide()

    def paintEvent(self, event):
        if not self._rect:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(0, 180, 255), 2, QtCore.Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))