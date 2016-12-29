#!/usr/bin/env python
# coding=utf-8
import sys
import config
from PyQt4 import QtCore,QtGui
from mainForm import MainForm

from helpForm import HelpForm




class Forms(QtGui.QWidget):
    def __init__(self, app):
        QtGui.QWidget.__init__(self)

        self.app = app
        self.setGeometry(QtCore.QRect(400, 300, 1024, 768))
        #self.setCursor(QtCore.Qt.BlankCursor)
        self.forms = dict()
        self.forms["MainForm"] = MainForm(self)
        self.forms["HelpForm"] = HelpForm(self)
        self.current_form = "MainForm"
        for form in self.forms.values():
            form.setFixedSize(config.Width, config.Height)
            form.hide()

        p = QtGui.QPalette()
        p.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
        self.setPalette(p)

    def get_form(self, wid):
        return self.forms.get(wid, -1)
    
    def show_form(self, wid):

        form = self.get_form(wid)
        if form == -1:
            print "no this form %s" % wid
            return -1

        self.current_form = wid
        
        form.show()

    def hide_form(self, wid):
        form = self.get_form(wid)
        if form == -1:
            print "no this form %s" % wid
            return -1

        form.hide()

    def destory_form(self, wid):
        form = self.get_form(wid)
        if form == -1:
            print "no this form %s" % wid
            return -1
        form.destory()

    def get_current_form(self):
        return self.get_form(self.current_form)

    def hide_current_form(self):
        self.hide_form(self.current_form)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    forms = Forms(app)
    forms.show_form('MainForm')

    forms.show()
    sys.exit(app.exec_())
