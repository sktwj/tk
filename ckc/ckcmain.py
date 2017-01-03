#!/usr/bin/env python
# coding=utf-8
import sys
import traceback
from ckc_controller import CKCController
#from tkiosk.utils import create_daemon

if __name__ == "__main__":
    try:
        ckc = CKCController()
        ckc.start()
        ckc.main_loop()
    except:
        print >> sys.stderr, "start ckc failed"
        print >> sys.stderr, traceback.format_exc()

