# -*- coding: utf-8 -*-

import os

LOG_FILE = "/tmp/opentunnel.log"


def log(message):
    """
    Write message to OpenTunnel log file.
    """

    try:
        with open(LOG_FILE, "a") as f:
            f.write("[OpenTunnel] %s\n" % message)
    except Exception:
        print("[OpenTunnel] %s" % message)