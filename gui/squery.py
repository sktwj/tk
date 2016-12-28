#!/usr/bin/env python
# coding=utf-8

import simplejson as json
from tkiosk.utils.ui_conn import UiClient
from tkiosk.utils.util import get_log



class socketQuery():

    def __init__(self):
        self.log = get_log()

    def setup(self):
        try:
            global socketq 
            socketq = UiClient()
            socketq.open()
            socetq.connect()
        except Exception, ex:
            print "socketquery exception: cannot connect %s" % str(ex)
            raise

        self.sd = socketq.sock

    def send(self, data):
        try:
            data = json.dumps(data)
            socketq.sock.send(str(len(data)) + "\n")
            socketq.sock.send(data)
            self.log.info("send data %s" % data)
        except Exception, ex:
            self.log.error("send ex %s" % str(ex))

    def trace(self):
        return trace

    def deinit(self):
        socketq.close()


