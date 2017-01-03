#!/usr/bin/env python
# coding=utf-8
import os
import socket
import fcntl
import simplejson

SOCK_FILE = "/tmp/usock"


class UiMessage(object):
    def __init__(self, *args, **kw):

        self.type = kw.get('type')
        self.cid = kw.get('cid')
        self.cmd = kw.get('cmd')
        self.param_info = kw.get('param_info')
        self.args = args
        self.wid = ''


    def loads(self, data):

        params = simplejson.loads(data)
        self.type = params.get('type') or "EVENT"
        self.cid = params.get('cid')
        self.cmd = params.get('cmd')
        self.wid = params.get('wid')
        self.param_info = params.get('param_info') or dict()
        self.args = tuple(params.get('args')) or ()

    def dumps(self):

        params = dict(type = self.type,
                      cid = self.cid,
                      cmd = self.cmd,
                      wid = self.wid,
                      param_info = self.param_info,
                      args = self.args)
        return simplejson.dumps(params)

    def __str__(self):
        return "{'type': %s, 'wid': %s, 'cid': %s, 'cmd': %s, 'param_info': %s, 'args': %s}" % (
            self.type, self.wid, self.cid, self.cmd, self.param_info, self.args)

class UiSocket(object):
    def __init__(self):
        self.port = 0
        self.sock = None
        self.msglen = 0
        self.msg = ""
        self.buffer = ""

    def open(self):
        pass

    def close(self):
        pass

    def recv_msg(self):
        if self.msg:
            msg = self._parse_tcp_stream()
            if msg:return msg
            while True:
                data = self.sock.recv(4096)
                if not data:
                    raise RuntimeError("socket conn broken")
                else:
                    msg = self._parse_tcp_stream(data)
                    if msg: return msg


    def send_msg(self, message):
        data = message.dumps()
        msg = "%s\n%s" % (len(data), data)
        self.sock.sendall(msg)

    def _parse_tcp_stream(self, data=""):
        self.buffer = ""
        self.msg += data
        if self.msglen == 0 and self.msg:
            try:
                i = self.msg.index("\n")
                self.msglen = int(self.msg[:i])
                self.msg = self.msg[i+1:]
            except:
                pass

        if self.msg and self.msglen > 0 and len(self.msg) >= self.msglen:
            self.buffer = self.msg[:self.msglen]
            self.msg = self.msg[self.msglen:]
            self.msglen = 0

        if self.buffer:
            msg = UiMessage()
            msg.loads(self.buffer)
            return msg
        else:
            return None

class UiServer(UiSocket):
    def __init__(self):
        super(UiServer, self).__init__()

    def open(self):
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        flag = fcntl.fcntl(self.server, fcntl.F_GETFD)
        '''set file keep open while program running'''
        fcntl.fcntl(self.server, fcntl.F_SETFD, flag or fcntl.FD_CLOEXEC)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    def close(self):
        if self.server:
            self.server.close()

        if self.sock:
            self.sock.close()

    def listen(self, file=SOCK_FILE):
        try:
            os.remove(file)
        except OSError:
            pass

        self.server.bind(file)
        self.server.listen(1)

    def accept(self):
        self.sock, self.addr = self.server.accept()

class UiClient(UiSocket):
    def __init__(self):
        super(UiClient, self).__init__()

    def open(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def close(self):
        if self.sock:
            self.sock.close()

    def connect(self, file=SOCK_FILE):
        self.sock.connect(file)


