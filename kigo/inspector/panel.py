# SPDX-License-Identifier: Zlib
# kigo/inspector/panel.py

from kigo.qt.backend import QtWidgets


class InspectorPanel(QtWidgets.QDockWidget):
    def __init__(self):
        super().__init__("Kigo Inspector")
        self.setAllowedAreas(
            self.DockWidgetArea.LeftDockWidgetArea
            | self.DockWidgetArea.RightDockWidgetArea
        )

        self.text = QtWidgets.QPlainTextEdit()
        self.text.setReadOnly(True)
        self.setWidget(self.text)

    def inspect(self, widget):
        if widget is None:
            self.text.setPlainText("No widget")
            return

        info = []
        info.append(f"Class: {widget.__class__.__name__}")
        info.append(f"ObjectName: {widget.objectName() or '(none)'}")
        info.append(f"Visible: {widget.isVisible()}")
        info.append(f"Enabled: {widget.isEnabled()}")
        info.append(f"Geometry: {widget.geometry()}")

        parents = []
        p = widget.parentWidget()
        while p:
            parents.append(p.__class__.__name__)
            p = p.parentWidget()

        info.append("Parent chain:")
        for name in parents:
            info.append(f"  ↳ {name}")

        self.text.setPlainText("\n".join(info))