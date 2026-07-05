# -*- coding: utf-8 -*-
from . import config

from Plugins.Plugin import PluginDescriptor

from .main import OpenTunnelScreen
from .logger import log
from .version import PLUGIN_NAME


def main(session, **kwargs):
    """Open the main OpenTunnel window."""
    log("Plugin started")
    session.open(OpenTunnelScreen)


def Plugins(**kwargs):
    """Register plugin in the Plugin menu."""
    return [
        PluginDescriptor(
            name=PLUGIN_NAME,
            description="SSH Tunnel Manager for Enigma2",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main
        )
    ]
