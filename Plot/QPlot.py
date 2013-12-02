#!/usr/bin/env python3

import sys
import socket
import time
from random import random as rand
from threading import Thread
from queue import Queue
from queue import Empty
from PySide import QtCore
from PySide.QtGui import *

class Reader(Thread, QtCore.QObject):
  speak = QtCore.Signal()

  def __init__(self, file_in, queue, nbr_data):
    Thread.__init__(self)
    QtCore.QObject.__init__(self)
    self._file_in = file_in
    self._queue = queue
    self._nbr_data = nbr_data
    self._nbr = 0
    self._running = False

  def run(self):
    self._running = True
    while self._running:
      line = self._file_in.readline().decode('ascii').strip().split(' ')
      if len(line) == self._nbr_data + 2 and line[0] == 'T':
        try:
          f = list(map(float, line[1:]))
        except ValueError:
          pass
        else:
          self._queue.put((f[0], f[1:]))
          # print(f)
          self._nbr += 1

          if self._nbr > 42 * 0.1:
            self.speak.emit()
            self._nbr = 0

  def stop(self):
    self._running = False

class PlotController(QWidget):
  def __init__(self, parent=None):
    super(PlotController, self).__init__(parent)

    self._plots = {}
    self._y_min = 0
    self._y_max = 0
    self._x_size = 100
    self._x_max = 0
    self._nbr_data = 9

    self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self._sock.connect('./test')
    self._file = self._sock.makefile('rb', buffering=0)
    self._queue = Queue()
    self._thread = Reader(self._file, self._queue, self._nbr_data)

    self._scene = QGraphicsScene()
    self._view = QGraphicsView(self._scene)
    self._view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self._view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    layout = QVBoxLayout()
    layout.addWidget(self._view)
    self.setLayout(layout)

    self.setWindowTitle("Plot")

    self._thread.speak.connect(self._read_data)
    self._thread.start()

  def _read_data(self):
    print('pute de merde', time.time(), self._queue.qsize())
    while True:
      try:
        t, data = self._queue.get_nowait()
      except Empty:
        return
      else:
        for id, d in enumerate(data):
          self.addPoint(id, t, d)

  def closeEvent(self, event):
    self.close()
    super(PlotController, self).closeEvent(event)

  def resizeEvent(self, event):
    self.fitInView()
    super(PlotController, self).resizeEvent(event)

  def close(self):
    self._thread.stop()
    self._thread.join()
    self._sock.close()
    self._file.close()

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

    if y < self._y_min or y > self._y_max:
      # self._x_max = max(self._x_max, x)
      self._y_min = min(self._y_min, y)
      self._y_max = max(self._y_max, y)
      self.fitInView()

  def fitInView(self):
      x = self._x_max - self._x_size
      h = self._y_max - self._y_min
      self._view.fitInView(x, self._y_min, self._x_size, h)

def testAddPoint(controller):
  import math
  f = lambda x, n: 10 * math.sin(x / 10.0 * n)
  for id in range(3):
    for x in range(200):
      controller.addPoint(id, x, f(x, id))

if __name__ == "__main__":
  app = QApplication(sys.argv)
  controller = PlotController()

  # testAddPoint(controller)

  controller.show()
  sys.exit(app.exec_())
