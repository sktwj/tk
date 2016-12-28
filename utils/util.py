#!/usr/bin/env python
# coding=utf-8

import logging
import logging.handlers


def get_log():
    LOG = logging.getLogger("ui")
    LOG.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(thread)d %(message)s')
    rotateHandle = logging.handlers.RotatingFileHandler("~/var/log/ui.log", maxBytes=1024*1024*10, backupCount=2)
    rotateHandle.setFormatter(formatter)
    LOG.addHandler(rotateHandle)
    return LOG
