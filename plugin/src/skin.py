# -*- coding: utf-8 -*-

"""
OpenTunnel Skin
"""

MAIN_SKIN = """
<screen name="OpenTunnelScreen"
    position="center,center"
    size="620,440"
    title="OpenTunnel">

    <widget name="config"
        position="10,10"
        size="600,330"
        scrollbarMode="showOnDemand"/>

    <widget name="status"
        position="15,350"
        size="590,25"
        font="Regular;22"
        halign="center"/>

    <widget source="key_red"
        render="Label"
        position="20,390"
        size="120,30"
        font="Regular;22"
        halign="center"/>

    <widget source="key_green"
        render="Label"
        position="170,390"
        size="120,30"
        font="Regular;22"
        halign="center"/>

    <widget source="key_yellow"
        render="Label"
        position="320,390"
        size="120,30"
        font="Regular;22"
        halign="center"/>

    <widget source="key_blue"
        render="Label"
        position="470,390"
        size="120,30"
        font="Regular;22"
        halign="center"/>

</screen>
"""