#!/usr/bin/env python
# coding=utf-8
import os
from Queue import Empty
from tkiosk.utils.util import init_log


class BaseForm(object):
    def __init__(self):

        self.state = self.__class__.__name__

        self.name = self.state

        self.backable = True
        self.id = "BS0"
        self.ctrller = None
        self.timeout = None
        self._widgets = dict()
