#!/usr/bin/env python3

import sys
from PySide import QtCore, QtGui

class PlotController(QtGui.QWidget):
  def __init__(self, parent=None):
    super(PlotController, self).__init__(parent)

    self._scene = QtGui.QGraphicsScene()
    self._view = QtGui.QGraphicsView(self._scene)

    self._scene.addRect(0, 0, 1, 1)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(self._view)
    self.setLayout(layout)

    self.setWindowTitle("Plot")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = PlotController()
    controller.show()
    sys.exit(app.exec_())
