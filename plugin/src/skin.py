# -*- coding: utf-8 -*-

MAIN_SKIN = """
<screen name="OpenTunnelScreen"
    position="center,center"
    size="760,520"
    title="OpenTunnel">

    <!-- Logo -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/logo.png"
        position="220,10"
        size="320,120"
        alphatest="blend" />

    <!-- Config -->
    <widget
        name="config"
        position="20,140"
        size="720,230"
        scrollbarMode="showOnDemand" />

    <!-- Separator -->
    <eLabel
        position="20,380"
        size="720,2"
        backgroundColor="#404040" />

    <!-- Status Icon -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/disconnected.png"
        position="20,392"
        size="32,32"
        alphatest="blend" />

    <!-- Status -->
    <widget
        source="status"
        render="Label"
        position="60,392"
        size="300,30"
        font="Regular;22"
        valign="center" />

    <!-- Version -->
    <widget
        source="version"
        render="Label"
        position="560,392"
        size="180,30"
        font="Regular;20"
        halign="right"
        valign="center" />

    <!-- RED -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/red.png"
        position="20,455"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_red"
        render="Label"
        position="72,466"
        size="90,22"
        font="Regular;20" />

    <!-- GREEN -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/green.png"
        position="190,455"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_green"
        render="Label"
        position="242,466"
        size="90,22"
        font="Regular;20" />

    <!-- YELLOW -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/yellow.png"
        position="360,455"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_yellow"
        render="Label"
        position="412,466"
        size="90,22"
        font="Regular;20" />

    <!-- BLUE -->
    <ePixmap
        pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/images/blue.png"
        position="530,455"
        size="48,48"
        alphatest="blend" />

    <widget
        source="key_blue"
        render="Label"
        position="582,466"
        size="120,22"
        font="Regular;20" />

</screen>
"""