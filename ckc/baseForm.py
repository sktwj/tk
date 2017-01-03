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
        self.gui_command = CGlobalCommand()
        self.addWidget(self.gui_command)

    def add_widget(self):
        widget.setForm(self)
        self._widgets[widget.name] = widget


    def set_controller(self, ctrller):
        self.ctrller = ctrller
        self.gs = ctrller.gs
        self.log = ctrller.log

    def set_next_state(self, new_state):
        
        if self.ctrller.forms[self.ctrller.active_state].name == self.ctrller.forms[new_state].name:
            self.ctrller.set_new_gui_form(False)
        else:
            self.ctrller.set_new_gui_form(True)

        self.ctrller.active_state = new_state

    def _has_new_state(self):
        return self.ctrller.active_state != self.state
    
    def _reset(self, goto=True):
        self.log.info(( " %s " % self.state).center(85, '-'))
        if len(self.gs._history) > 0 and self.gs._history[-1].form_state == self.state:
            pass
        else:
            self.gs.add_history(self.state)

        self.reset_form()
        if self.goto:
            self.gui_command.gotoWindow(wid=self.name)
    
    def reset_form(self):
        pass
    
    def start_job(self):
        pass

    def event_loop(self):
        while not self._has_new_state():
            try:
                msg = self.ctrller.inputQ.get(timeout=self.timeout)
                if msg.type == "SOCKERROR":
                    raise Exception("gui socket connection broken")
                else:
                    if msg.wid == "Languageform":
                        self._set_language(**message.form_info)
                        self._reset()
                    elif msg.wid != self.name:
                        pass

                    else:
                        self._widgets[message.cid].callback(*msg.args, **message.param_info)
            except Empty:
                self.on_timeout()

    def render(self, goto=True):
        try:
            try:
                self._reset(goto)
                self.event_loop()
            finally:
                self.hide()
        except Exception, ex:
            self.log.error("failed to render %s %s" % (self.state, traceback.format_exc()))
            self.gs.reset()
            self.gs.exception = ex
            if self.ctrller.active_state != "FatalErrorForm":
                self.set_next_state("FatalErrorForm")

    def on_timeout(self):
        self.gs.reset()
        self.set_next_state("MainForm")

    def hide(self):
        pass

    
    def on_back(self, *args, **kwargs):
        while True:
            history = self.gs.pop_history()
            self.log.info("go back to %s" % history)
            if self.ctrller.forms[history].backable:
                self.set_next_state(history)
                break

class BaseMainForm(BaseForm):
    def __init__(self):
        super(BaseMainForm, self).__init__()
        self.timeout = 50

    def reset_form(self):
        super(BaseMainForm, self).reset_form()

    


