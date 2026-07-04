# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry

from .version import VERSION
from .logger import log


class OpenTunnelScreen(Screen, ConfigListScreen):

    skin = """
    <screen name="OpenTunnelScreen"
        position="center,center"
        size="750,520"
        title="OpenTunnel">

        <widget name="config"
            position="20,20"
            size="710,420"
            scrollbarMode="showOnDemand"/>

    </screen>
    """

    def __init__(self, session):

        Screen.__init__(self, session)

        self.setTitle("OpenTunnel v%s" % VERSION)

        self.list = [

            getConfigListEntry(
                "SSH Server",
                config.plugins.opentunnel.server
            ),

            getConfigListEntry(
                "SSH Port",
                config.plugins.opentunnel.port
            ),

            getConfigListEntry(
                "Username",
                config.plugins.opentunnel.username
            ),

            getConfigListEntry(
                "Password",
                config.plugins.opentunnel.password
            ),

            getConfigListEntry(
                "Auto Connect",
                config.plugins.opentunnel.autoconnect
           