# -*- coding: utf-8 -*-

MAIN_SKIN = """
<screen name="OpenTunnelScreen"
    position="center,center"
    size="760,500"
    title="OpenTunnel">

    <!-- Logo -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/logo.png"
        position="220,10"
        size="320,120"
        alphatest="blend" />

    <!-- Config List -->
    <widget
        name="config"
        position="20,140"
        size="720,250"
        scrollbarMode="showOnDemand" />

    <!-- Status Icon -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/disconnected.png"
        position="20,405"
        size="32,32"
        alphatest="blend" />

    <!-- Status Text -->
    <widget
        source="status"
        render="Label"
        position="60,405"
        size="250,32"
        font="Regular;22" />

    <!-- Red -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/red.png"
        position="20,450"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_red"
        render="Label"
        position="72,458"
        size="90,24"
        font="Regular;20" />

    <!-- Green -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/green.png"
        position="180,450"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_green"
        render="Label"
        position="232,458"
        size="90,24"
        font="Regular;20" />

    <!-- Yellow -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/yellow.png"
        position="340,450"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_yellow"
        render="Label"
        position="392,458"
        size="90,24"
        font="Regular;20" />

    <!-- Blue -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/blue.png"
        position="500,450"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_blue"
        render="Label"
        position="552,458"
        size="120,24"
        font="Regular;20" />

</screen>
"""