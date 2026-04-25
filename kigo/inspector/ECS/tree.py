from kigo.qt.backend import QtWidgets, QtCore

class EntityTree(QtWidgets.QTreeWidget):
    entitySelected = QtCore.Signal(object)

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.setHeaderLabels(["Entity"])
        self.refresh()
        self.itemClicked.connect(self.on_click)

    def refresh(self):
        self.clear()
        for eid in self.world.entities:
            QtWidgets.QTreeWidgetItem(self, [str(eid)])

    def on_click(self, item):
        self.entitySelected.emit(item.text(0))