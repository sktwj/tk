
import sys,os
import traceback
from PyQt4 import QtCore,QtGui
from control import MainControl

class MainApp(QtGui.QApplication):
    def __init__(self, argv):
        QtGui.QApplication.__init__(self, argv)

        self.control = MainControl()

    def exec_cmd(self, cmd):

        try:
            self.control.log.info(cmd)

            exec(cmd)
        except Exception, ex:
            self.control.log.error("exec cmd %s" % str(ex))
            self.control.log.error("exec cmd %s" % str(traceback.format_exc()))
            #print

    def exit_normal(self):
        sys.exit()

    def init_gui(self, param={}):
        pass



if __name__ == "__main__":
    app = MainApp(sys.argv)
    app.setFont(QtGui.QFont("Arial, WenQuanYi Micro Hei"))
    app.connect(app.control, QtCore.SIGNAL("exec_cmd(QString)"), app.exec_cmd)

    app.control.start()
    sys.exit(app.exec_())

