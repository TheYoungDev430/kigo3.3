from kigo.qt.backend import QtWidgets
from kigo.inspector.ecs.tree import EntityTree
from kigo.inspector.ecs.panel import ComponentPanel

class ECSInspector(QtWidgets.QDockWidget):
    def __init__(self, world):
        super().__init__("ECS Inspector")
        self.world = world

        splitter = QtWidgets.QSplitter()

        self.tree = EntityTree(world)
        self.panel = ComponentPanel()

        self.tree.entitySelected.connect(self.panel.inspect)

        splitter.addWidget(self.tree)
        splitter.addWidget(self.panel)
        self.setWidget(splitter)