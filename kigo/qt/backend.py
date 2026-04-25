# kigo/qt/backend.py
import sys

IS_ANDROID = hasattr(sys, "getandroidapilevel")

if IS_ANDROID:
    from PySide6 import QtCore, QtGui, QtWidgets
    QT_BACKEND = "pyside"
else:
    from PyQt6 import QtCore, QtGui, QtWidgets
    QT_BACKEND = "pyqt"

    __all__ = ["QtCore", "QtGui", "QtWidgets", "QT_BACKEND", "IS_ANDROID"]
