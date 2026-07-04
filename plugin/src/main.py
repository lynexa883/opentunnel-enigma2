# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.config import getConfigListEntry, config
from Components.Sources.StaticText import StaticText

from .version import VERSION
from .logger import log


class OpenTunnelScreen(Screen, ConfigListScreen):

    skin = """
    <screen name="OpenTunnelScreen"
        position="center,center"
        size="620,440"
        title="OpenTunnel">

        <widget name="config"
            position="10,10"
            size="600,340"
            scrollbarMode="showOnDemand"/>

        <widget source="key_red"
            render="Label"
            position="20,390"
            size="120,30"
            font="Regular;22"
            halign="center"
            valign="center"/>

        <widget source="key_green"
            render="Label"
            position="170,390"
            size="120,30"
            font="Regular;22"
            halign="center"
            valign="center"/>

        <widget source="key_yellow"
            render="Label"
            position="320,390"
            size="120,30"
            font="Regular;22"
            halign="center"
            valign="center"/>

        <widget source="key_blue"
            render="Label"
            position="470,390"
            size="120,30"
            font="Regular;22"
            halign="center"
            valign="center"/>

    </screen>
    """

    def __init__(self, session):

        Screen.__init__(self, session)

        self.setTitle("OpenTunnel v%s" % VERSION)

        self["key_red"] = StaticText("Cancel")
        self["key_green"] = StaticText("Save")
        self["key_yellow"] = StaticText("Test")
        self["key_blue"] = StaticText("Connect")

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
            )

        ]

        ConfigListScreen.__init__(self, self.list)

        self["actions"] = ActionMap(
            ["SetupActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "red": self.cancel,
                "green": self.save,
                "yellow": self.testConnection,
                "blue": self.connectTunnel,
                "ok": self.save
            },
            -2
        )

        log("Main screen opened")

    def save(self):

        for item in self["config"].list:
            item[1].save()

        log("Configuration saved")

        self.close()

    def cancel(self):

        for item in self["config"].list:
            item[1].cancel()

        log("Configuration canceled")

        self.close()

    def testConnection(self):

        log("Test connection requested")

    def connectTunnel(self):

        log("Connect tunnel requested")