#!/usr/bin/env python
# coding=utf-8

import traceback
import threading
from Queue import Queue
from ui_proxy import UiProxy
from ckc_config import KIOSK_FORMS, INIT_FORM
from tkiosk.utils.util import init_log


class CKCController(object):
    (ST_OK, ST_FAILURE, ST_INVALID) = range(3)
    def __init__(self):
        self.forms = dict()
        self.inputQ = Queue()
        self.outputQ = Queue()
        self.gs = GlobalSession()
        self.active_state = None
        self.log = init_log("ckc")
        self._gotonew = True
        self.condition = threading.Condition()


    def add_form_list(self, forms):
        self.log.info("initialize all forms.")
        for form in forms:
            cmd = "from gui%(form)s import %(form)s" % {"form": form}
            self.log.info("add form: %s" % cmd)
            exec(cmd)
            instance = None
            cmd = "instance = %s()" % form
            exec(cmd)
            self._add_form(instance)

    def add_form(self, form):

        if self.forms.get(form.state):
            raise Exception("repeat form..")
        self.forms[form.state] = form
        form.set_controller(self)

    def start(self):
        self.ui = UiProxy(self.inputQ, self.outputQ)
        self.ui.init_server()
        self.ui.start()
        self.add_form_list(KIOSK_FORMS)
        self.active_state = INIT_FORM

    def set_new_gui_form(self, v):
        self._gotonew = v

    def send(self, msg):
        self.outputQ.put(msg)

    def main_loop(self):
        self.log.debug("start main loop...")
        while self.status == CKCController.ST_OK:
            try:
                self.forms[self.active_state].render(self._gotonew)
            except KeyboardInterrupt:
                self.stop(0)
            except:
                self.log.error("%s" % traceback.format_exc())
                self.stop(-1)

        self.log.warning("exit ckc mainloop")
        self.stop(-2)

    def set_failure(self):
        self.log.warning("ckc is failure...")
        self.status = CKCController.ST_FAILURE


    def stop(self, status):
        self.log.warning("exiting ui..")
        self.ui.stop()

        sys.exit(status)

class GlobalSession(object):
    def __init__(self):
        self.reset()
        self.last_form = None

    def reset(self):
        self.args = tuple()
        self.kwargs = dict()
        self._history = list()
        self._goback = False
        self.last_form = None
        self.exception = None

    def add_history(self, form_state):
        self._goback = False
        self._history.append(History(form_state, self.args, self.kwargs))

    def reset_history(self, form_state):
        self._goback = False
        self._history.pop()
        self._history.append(History(form_state, self.args, self.kwargs))

    def pop_history(self):
        self._goback = True
        try:
            #pop current form
            history = self._history.pop()
            #pop last form

            history = self._history.pop()

            self.args = history.args
            self.kwargs = history.kwargs
            return history.form_state
        except IndexError:
            return "MainForm"

    def clean_history(self):
        self._history = list()


class History(object):
    def __init__(self, form_state, args, kwargs):
        self.form_state = form_state
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return "%s:%s" % (self.form_state, self.kwargs)






































