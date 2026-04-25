from kigo.qt.backend import QtWidgets

class ComponentPanel(QtWidgets.QPlainTextEdit):
    def inspect(self, entity_id):
        self.setPlainText(f"Components for entity {entity_id}")