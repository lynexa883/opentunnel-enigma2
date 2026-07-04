# -*- coding: utf-8 -*-

from .logger import log


class SSHManager(object):

    def __init__(self):
        self.connected = False

    def connect(self, host, port, username, password):
        """
        Connect to SSH server.
        """

        log("Connecting to %s:%s" % (host, port))

        # اتصال واقعی در مرحله بعد
        self.connected = False

        return self.connected

    def disconnect(self):

        if self.connected:
            log("Disconnected")

        self.connected = False

    def is_connected(self):

        return self.connected