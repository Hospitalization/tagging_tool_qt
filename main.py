#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
# @Author : heim (heim@laonbud.com)
# @Link   :
# @Date   : 2019-3-6
"""
.ui 을 pyuic로 변환하여 사용
"""
import sys
import os
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QPainter, QPen
from ui import ui_main


class Form(QtWidgets.QDialog):
    mouse_x = 0
    mouse_y = 0

    loaded = False

    images = []
    length = 0
    resize_ratio = 1
    current_frame = 0

    tag_list = []

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = ui_main.Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

        # signal 연결
        self.ui.pushButton_open_dir.clicked.connect(self.open_dir)
        self.ui.pushButton_convert.clicked.connect(self.open_file)
        self.ui.horizontalSlider.valueChanged.connect(self.slide_changed)
        self.ui.pushButton_next.clicked.connect(self.next_frame)
        self.ui.pushButton_prev.clicked.connect(self.prev_frame)

        # mouse 사용
        self.setMouseTracking(True)

        self.widgets = [
            self.ui.pushButton_prev,
            self.ui.pushButton_next,
            # self.ui.pushButton_add_class,
            # self.ui.pushButton_auto_track,
            # self.ui.pushButton_load,
            # self.ui.pushButton_save,
            # self.ui.pushButton_undo,
            self.ui.comboBox_class,
            # self.ui.comboBox_type,
            self.ui.horizontalSlider,
            self.ui.listWidget
        ]

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory()
        if dir_name:
            files_list = os.listdir(dir_name)
            files_list = sorted(files_list)
            self.images = []
            self.length = len(files_list)
            for file in files_list:
                pixmap = QPixmap(dir_name + "/" + file)
                pixmap = pixmap.scaledToWidth(self.ui.label.width())
                self.images.append(pixmap)
                print("{} is loaded.".format(file))
                self.tag_list.append([])
            self.resize_ratio = self.ui.label.width() / pixmap.width()
            # self.ui.label.setPixmap(self.images[0])
            self.ui.label.resize(pixmap.width(), pixmap.height())

            # initialize slider
            self.ui.horizontalSlider.setMinimum(0)
            self.ui.horizontalSlider.setMaximum(self.length - 1)
            self.ui.horizontalSlider.setValue(0)
            self.slide_changed()

            self.loaded = True

            self.ui.label.loaded = True
            self.ui.label.tags = self.tag_list[self.current_frame]
            self.ui.label.resize_ratio = self.resize_ratio
            self.ui.label.image = self.images[self.current_frame]

            self.enable(self.widgets)
            print(self.ui.label.geometry())

    def enable(self, widgets):
        for widget in widgets:
            widget.setEnabled(True)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            return file_name

    def slide_changed(self):
        self.current_frame = self.ui.horizontalSlider.value()
        self.ui.label_frame.setText(str(self.current_frame + 1) + '/' + str(self.length))
        # self.ui.label.setPixmap(self.images[self.current_frame])

        self.ui.listWidget.clear()
        self.update_list()

    def next_frame(self):
        self.current_frame = self.ui.horizontalSlider.value()
        self.ui.horizontalSlider.setValue(self.current_frame + 1)
        self.ui.listWidget.clear()
        self.update_list()

    def prev_frame(self):
        self.current_frame = self.ui.horizontalSlider.value()
        self.ui.horizontalSlider.setValue(self.current_frame - 1)
        self.ui.listWidget.clear()
        self.update_list()

    def update_list(self):
        self.ui.listWidget.clear()
        tags = self.tag_list[self.current_frame]
        if len(tags) != 0:
            for tag in tags:
                item = QListWidgetItem(str(tag))
                self.ui.listWidget.addItem(item)

        self.ui.label.tags = self.tag_list[self.current_frame]
        self.ui.label.image = self.images[self.current_frame]

        self.ui.label.repaint()

    def mouseMoveEvent(self, me: QtGui.QMouseEvent):
        self.mouse_x = me.x() - self.ui.label.geometry().x()
        self.mouse_y = me.y() - self.ui.label.geometry().y()
        if 0 <= self.mouse_x < self.ui.label.geometry().width() and 0 <= self.mouse_y < self.ui.label.geometry().height():
            self.ui.label_mouse_position.setText('{}/{}'.format(self.mouse_x, self.mouse_y))
            self.update()
        # self.ui.label_mouse_position.setText('{}/{}'.format(self.ui.label.mouse_x, self.ui.label.mouse_y))

    def mousePressEvent(self, me: QtGui.QMouseEvent):
        self.mouse_x = me.x() - self.ui.label.geometry().x()
        self.mouse_y = me.y() - self.ui.label.geometry().y()
        if self.length and 0 <= self.mouse_x < self.ui.label.geometry().width() and 0 <= self.mouse_y < self.ui.label.geometry().height():
            cls = self.ui.comboBox_class.currentText()
            pos = [cls, self.mouse_x, self.mouse_y]
            self.tag_list[self.current_frame].append(pos)
            self.update_list()

    def keyPressEvent(self, ke: QtGui.QKeyEvent):
        key = ke.key()

        if key == QtCore.Qt.Key_Left:
            self.prev_frame()
        elif key == QtCore.Qt.Key_Right:
            self.next_frame()
        elif key == QtCore.Qt.Key_Delete:
            idx = self.ui.listWidget.currentRow()
            if idx is not None and len(self.tag_list[self.current_frame]):
                self.tag_list[self.current_frame].pop(idx)
                self.update_list()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
