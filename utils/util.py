#!/usr/bin/env python
# coding=utf-8

import logging
import logging.handlers
KIOSK_PATH="/home/t/"

def init_log(log_name):
    LOG = logging.getLogger(log_name)
    LOG.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(thread)d %(message)s')
    rotateHandle = logging.handlers.RotatingFileHandler(KIOSK_PATH + "var/log/%s.log" % log_name, maxBytes=1024*1024*10, backupCount=2)
    rotateHandle.setFormatter(formatter)
    LOG.addHandler(rotateHandle)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    LOG.addHandler(ch)
    return LOG
