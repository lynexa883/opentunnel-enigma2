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

        #
        # Color Buttons
        #
        self["key_red"] = StaticText(_("Cancel") if "_" in globals() else "Cancel")
        self["key_green"] = StaticText(_("Save") if "_" in globals() else "Save")
        self["key_yellow"] = StaticText(_("Test") if "_" in globals() else "Test")
        self["key_blue"] = StaticText(_("Connect") if "_" in globals() else "Connect")

        #
        # Status
        #
        self["status"] = Label("Disconnected")

        #
        # Version
        #
        self["version"] = Label("Version %s" % VERSION)

        #
        # Config List
        #
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

        #
        # Actions
        #
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

        log("OpenTunnel main screen loaded")

    # ------------------------------------------------

    def setStatus(self, text):

        self["status"].setText(text)
        log("Status: %s" % text)

    # ------------------------------------------------

    def save(self):

        for item in self["config"].list:
            item[1].save()

        self.setStatus("Configuration Saved")

        self.close()

    # ------------------------------------------------

    def cancel(self):

        for item in self["config"].list:
            item[1].cancel()

        self.setStatus("Canceled")

        self.close()

    # ------------------------------------------------

    def testConnection(self):

        self.setStatus("Testing SSH...")

        log("Test button pressed")

    # ------------------------------------------------

    def connectTunnel(self):

        self.setStatus("Connecting...")

        log("Connect button pressed")