# -*- coding: utf-8 -*-

from Components.config import (
    config,
    ConfigSubsection,
    ConfigText,
    ConfigPassword,
    ConfigInteger,
    ConfigYesNo
)

# Create OpenTunnel configuration section
config.plugins.opentunnel = ConfigSubsection()

# SSH Server Address
config.plugins.opentunnel.server = ConfigText(
    default="",
    fixed_size=False
)

# SSH Port
config.plugins.opentunnel.port = ConfigInteger(
    default=22,
    limits=(1, 65535)
)

# SSH Username
config.plugins.opentunnel.username = ConfigText(
    default="root",
    fixed_size=False
)

# SSH Password
config.plugins.opentunnel.password = ConfigPassword(
    default=""
)

# Auto Connect on Enigma2 Startup
config.plugins.opentunnel.autoconnect = ConfigYesNo(
    default=False
)