# -*- coding: utf-8 -*-

"""
OpenTunnel Configuration
"""

from Components.config import (
    config,
    ConfigSubsection,
    ConfigText,
    ConfigPassword,
    ConfigInteger,
    ConfigYesNo
)

config.plugins.opentunnel = ConfigSubsection()

# SSH Server
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

# Connect automatically after Enigma2 starts
config.plugins.opentunnel.autoconnect = ConfigYesNo(
    default=False
)