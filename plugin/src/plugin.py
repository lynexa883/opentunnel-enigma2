# -*- coding: utf-8 -*-

from Plugins.Plugin import PluginDescriptor

from .main import OpenTunnelScreen
from .logger import log


def main(session, **kwargs):

    log("Plugin Started")

    session.open(OpenTunnelScreen)


def Plugins(**kwargs):

    return [
        PluginDescriptor(
            name="OpenTunnel",
            description="SSH Tunnel Manager for Enigma2",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main
        )
    ]