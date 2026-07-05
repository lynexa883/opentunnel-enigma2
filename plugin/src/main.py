# -*- coding: utf-8 -*-

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.config import getConfigListEntry, config
from Components.Sources.StaticText import StaticText
from Components.Label import Label

from .skin import MAIN_SKIN
from .version import VERSION
from .logger import log


class OpenTunnelScreen(Screen, ConfigListScreen):

    skin = MAIN_SKIN

    def __init__(self, session):

        Screen.__init__(self, session)

        self.setTitle("OpenTunnel v%s" % VERSION)

        # Color Buttons
        self["key_red"] = StaticText("Cancel")
        self["key_green"] = StaticText("Save")
        self["key_yellow"] = StaticText("Test")
        self["key_blue"] = StaticText("Connect")

        # Status Label
        self["status"] = Label("Status : Disconnected")

        # Configuration List
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

    def setStatus(self, text):
        self["status"].setText("Status : %s" % text)

    def save(self):

        for item in self["config"].list:
            item[1].save()

        self.setStatus("Configuration Saved")

        log("Configuration saved")

        self.close()

    def cancel(self):

        for item in self["config"].list:
            item[1].cancel()

        self.setStatus("Canceled")

        log("Configuration canceled")

        self.close()

    def testConnection(self):

        self.setStatus("Testing Connection...")

        log("Test connection requested")

    def connectTunnel(self):

        self.setStatus("Connecting...")

        log("Connect tunnel requested")