from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush


class customLabel(QtWidgets.QLabel):
    mouse_x = 0
    mouse_y = 0

    loaded = False

    image = None
    resize_ratio = 1

    tags = []

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)

    def paintEvent(self, pe: QtGui.QPaintEvent):
        if self.loaded:
            painter = QPainter(self)
            pixmap = self.image
            painter.drawPixmap(self.rect(), pixmap)
            if self.tags:
                pen = QPen(QtCore.Qt.red)
                pen.setWidth(3)
                painter.setPen(pen)
                for tag in self.tags:
                    # painter.drawPoint(tag[1], tag[2])
                    painter.drawEllipse(QtCore.QPoint(tag[1], tag[2]), 1.5, 1.5)

    # def mouseMoveEvent(self, me: QtGui.QMouseEvent):
    #     self.mouse_x = me.x()
    #     self.mouse_y = me.y()
