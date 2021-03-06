#!/usr/bin/env python
# coding=utf-8
import os
from PyQt4 import QtCore

from squery import socketQuery



class MainControl(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)
        self.sock = socketQuery()
        self.log = self.sock.log

    def init_gui(self, params=dict()):
        self.emit(QtCore.SIGNAL("exec_cmd(QString)"), "self.init_gui("+str(param)+")")

    def rev_data(self):
        while True:
            try:
                r,w,e = select.select([self.sock.sd], [], [], 0.0001)
                if self.sock.sd in r:
                    full_data = ""
                    try:
                        length = ''
                        while True:
                            '''
                            recv packet length
                            '''
                            data = self.sock.sd.recv(1)
                            if (data == "\n"):
                                break
                            length = length + data
                        len_data = 0
                        '''
                        recv packet data by length
                        '''
                        while (len_data != int(length)):
                            data = self.sock.sd.recv(int(length) - len(data))
                            len_data += len(data)
                            full_data = full_data + data
                        if full_data:
                            self.process(full_data)
                    except Exception, ex:
                        self.log.error("recv_data error when recv %s" % str(ex))
            except Exception, ex:
                self.log.error("rev_data error when select data %s" % str(ex))

    def process(self, data):
        self.log.info("processing %s" % data)

    def run(self):
        i = 0
        while True:
            try:
                i += 1
                self.sock.setup()
                ## test if sock server is ok...
                break
            except:
                if i < 10:
                    time.sleep(2)
                    continue
                else:
                    os.exit(-1)
        self.rev_data()

#
if __name__ == "__main__":
    pass
