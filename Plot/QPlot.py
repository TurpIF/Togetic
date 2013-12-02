#!/usr/bin/env python3

import sys
from random import random as rand
from PySide import QtCore
from PySide.QtGui import *

class PlotController(QWidget):
  def __init__(self, parent=None):
    super(PlotController, self).__init__(parent)

    self._plots = {}
    self._y_min = 0
    self._y_max = 0
    self._x_size = 100
    self._x_max = 0

    self._scene = QGraphicsScene()
    self._view = QGraphicsView(self._scene)
    self._view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self._view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    layout = QVBoxLayout()
    layout.addWidget(self._view)
    self.setLayout(layout)

    self.setWindowTitle("Plot")

  def resizeEvent(self, event):
    self.fitInView()
    super(PlotController, self).resizeEvent(event)

  def addPoint(self, id, x, y):
    if not id in self._plots:
      color = QColor(rand() * 255, rand() * 255, rand() * 255)
      pos = x, y
      pen = QPen(QBrush(color), 0, QtCore.Qt.SolidLine,
          QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
      self._plots[id] = pen, pos
    else:
      color, pos = self._plots[id]
      self._plots[id] = color, (x, y)
      self._scene.addLine(pos[0], pos[1], x, y, color)

    if x > self._x_max \
      or y < self._y_min or y > self._y_max:
      self._x_max = max(self._x_max, x)
      self._y_min = min(self._y_min, y)
      self._y_max = max(self._y_max, y)
      self.fitInView()

  def fitInView(self):
      x = self._x_max - self._x_size
      h = self._y_max - self._y_min
      self._view.fitInView(x, self._y_min, self._x_size, h)

def testAddPoint(controller):
  import math
  f = lambda x, n: 10 * math.sin(x * n)
  for id in range(5):
    for x in range(200):
      controller.addPoint(id, x, f(x, id))

if __name__ == "__main__":
  app = QApplication(sys.argv)
  controller = PlotController()

  testAddPoint(controller)

  controller.show()
  sys.exit(app.exec_())
