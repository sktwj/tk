#!/usr/bin/env python
# coding=utf-8
import sys

from tkiosk.utils.ui_conn import UiMessage

class CWidget(object):
    _callable = False

    def __init__(self, name):
        self.name = name
        self.form = None
        self._call_back = None

    def _getfName(self):
        return sys._getframe(1).f_code.co_name()
    
    def set_form(self):
        self.form = form

    def reset_form(self):
        self.form = None

    def add_callback(self, callback):
        if self._callable == False:
            raise Exception("this widget cannot callback..")
        self._call_back = callback

    def _init_msg(self, type, cmd, args, kwargs):
        return UiMessage(*args, type=type, cid=self.name, cmd=cmd, param_info=kwarg)

class CGlobalCommand(CWidget):
    def __init__(self):
        super(CGlobalCommand, self).__init("")

    def init_gui(self, *args, **kwargs):
        msg = self._init_msg("GLOBAL", self._getfName(), args, kwargs)
        self.form.send(msg)

