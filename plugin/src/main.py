# -*- coding: utf-8 -*-

from Screens.Screen import Screen

from Components.ActionMap import ActionMap
from Components.Label import Label

from .version import VERSION
from .logger import log


class OpenTunnelScreen(Screen):

    skin = """
    <screen name="OpenTunnelScreen"
        position="center,center"
        size="600,400"
        title="OpenTunnel">

        <widget name="title"
            position="20,20"
            size="560,40"
            font="Regular;28"
            halign="center"/>

        <widget name="info"
            position="20,80"
            size="560,40"
            font="Regular;22"
            halign="center"/>

        <widget name="status"
            position="20,340"
            size="560,30"
            font="Regular;20"
            halign="center"/>

    </screen>
    """

    def __init__(self, session):

        Screen.__init__(self, session)

        log("Main screen created")

        self["title"] = Label("OpenTunnel v%s" % VERSION)

        self["info"] = Label("SSH Tunnel Manager")

        self["status"] = Label("Status : Disconnected")

        self["actions"] = ActionMap(
            ["OkCancelActions"],
            {
                "cancel": self.close
            },
            -1
        )

    def close(self):

        log("Plugin Closed")

        Screen.close(self)