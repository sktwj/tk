#!/usr/bin/env python
# coding=utf-8
import sys
import os
from PyQt4 import QtGui, QtCore
from squery import socketQuery
import config


class MainForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.parent = parent
        self.wid = "MainForm"
        self.sq = socketQuery()
        self.setAutoFillBackground(True)

        self.btn = QtGui.QPushButton("mainBtn", self)
        self.btn.clicked.connect(self.send)
        l = QtGui.QHBoxLayout()
        l.addWidget(self.btn)
        self.setLayout(l)

    def send(self):

        data = dict(wid=self.wid,
                    cid='mainBtn',
                    type='EVENT',
                   EVENT='EVENT_MOUSE_CLICK',
                   param_info={})
        print data
        self.sq.send(data)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = MainForm()
    a.show()
    sys.exit(app.exec_())
