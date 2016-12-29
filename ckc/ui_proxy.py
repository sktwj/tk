#!/usr/bin/env python
# coding=utf-8

import time
from threading import Thread 
from tkiosk.utils import UiServer, UiMessage
from tkiosk.utils.util import init_log

class UiProxy(object):
    RUNNING, STOP, WAITING = range(3)

    def __init__(self, inputQ, outputQ):
        self.inputQ = inputQ
        self.guiReady = False
        self.outputQ = outputQ
        self.server = UiServer()
        self.log = init_log("ui_proxy")
        self._state = UiProxy.RUNNING
        self.running_thread = list()

    def init_server(self):
        try:
            self.server.open()
            self.server.listen()
        except:
            self.log.error("server socket init failed %s " % traceback.format_exc())
            raise

    def _recv(self):
        try:
            self.server.accept()
            self.guiReady = True
            while self._state == UiProxy.RUNNING:
                try:
                    msg = self.server.recv_msg()
                except:
                    self.log.info("gui disconnect, wait for gui connect")
                    self._state = UiProxy.WAITING
                    self.server.accept()
                    self._state = UiProxy.RUNNING
                    continue

                self.log.info("get cmd %s" % repr(msg))

                self.process(msg)

        except:
            if self._state == UiProxy.RUNNING:
                self.log.error("server get command %s" % self.server.buffer)
                self.log.error("server recv failed %s" % traceback.format_exc())

    def process(self, msg):
        self.log.info("recv msg %s" % msg)

        self.inputQ.put(msg)





