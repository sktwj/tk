#!/usr/bin/env python
# coding=utf-8
import sys
import os
from PyQt4 import QtGui, QtCore
from squery import socketQuery
import config


class HelpForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.parent = parent
        self.wid = "HelpForm"
        self.sq = socketQuery()
        self.setAutoFillBackground(True)

        self.btn = QtGui.QPushButton("help me", self)
        self.btn.clicked.connect(self.send)
        l = QtGui.QHBoxLayout()
        l.addWidget(self.btn)
        self.setLayout(l)

    def send(self):

        data = dict(wid=self.wid,
                    cid='helpBtn',
                    type='EVENT',
                   EVENT='EVENT_MOUSE_CLICK',
                   param_info={})
        self.sq.send(data)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = HelpForm()
    a.show()
    sys.exit(app.exec_())
