#!/usr/bin/env python3

import sys
from random import random as rand
from PySide import QtCore
from PySide.QtGui import *

class PlotController(QWidget):
  def __init__(self, parent=None):
    super(PlotController, self).__init__(parent)

    self._pens = {}

    self._scene = QGraphicsScene()
    self._view = QGraphicsView(self._scene)

    layout = QVBoxLayout()
    layout.addWidget(self._view)
    self.setLayout(layout)

    self.setWindowTitle("Plot")

  def addPoint(self, id, x, y):
    if not id in self._pens:
      color = QColor(rand() * 255, rand() * 255, rand() * 255)
      self._pens[id] = QPen(color)
    self._scene.addRect(x, y, 1, 1, self._pens[id])

def testAddPoint(controller):
  import math
  f = lambda x, n: 10 * math.sin(x * n)
  for id in range(5):
    for x in range(100):
      controller.addPoint(id, x, f(x, id))

if __name__ == "__main__":
  app = QApplication(sys.argv)
  controller = PlotController()

  testAddPoint(controller)

  controller.show()
  sys.exit(app.exec_())
