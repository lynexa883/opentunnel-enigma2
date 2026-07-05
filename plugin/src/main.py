# -*- coding: utf-8 -*-

import time

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.config import config, configfile, getConfigListEntry
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from enigma import eTimer

from .skin import MAIN_SKIN
from .version import VERSION
from .logger import log
from .ssh import (
    SSHClient,
    MSG_CONNECTED,
    MSG_FAILED,
    MSG_DISCONNECTED,
    MSG_TEST_OK,
    MSG_TEST_FAIL,
)

POLL_MS = 250
MONITOR_MS = 2000
STATUS_HOLD_MS = 3000


class OpenTunnelScreen(Screen, ConfigListScreen):

    skin = MAIN_SKIN

    def __init__(self, session):

        Screen.__init__(self, session)

        self.setTitle("OpenTunnel v%s" % VERSION)

        # SSH engine
        self.ssh = SSHClient()

        # State
        self.closing = False
        self.busy_action = None   # None / "test" / "connect" / "disconnect"
        self._status_text = ""
        self._status_hold_until = 0

        # Buttons
        self["key_red"] = StaticText("Cancel")
        self["key_green"] = StaticText("Save")
        self["key_yellow"] = StaticText("Test")
        self["key_blue"] = StaticText("Connect")

        # Labels
        self["status"] = Label("Disconnected")
        self["version"] = Label("Version %s" % VERSION)

        # Config list
        self.list = [
            getConfigListEntry("SSH Server", config.plugins.opentunnel.server),
            getConfigListEntry("SSH Port", config.plugins.opentunnel.port),
            getConfigListEntry("Username", config.plugins.opentunnel.username),
            getConfigListEntry("Password", config.plugins.opentunnel.password),
            getConfigListEntry("Auto Connect", config.plugins.opentunnel.autoconnect),
        ]

        ConfigListScreen.__init__(self, self.list)

        # Actions
        self["actions"] = ActionMap(
            ["SetupActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "red": self.cancel,
                "green": self.save,
                "yellow": self.testConnection,
                "blue": self.toggleTunnel,
                "ok": self.save,
            },
            -1
        )

        self.onClose.append(self.cleanup)
        self.onLayoutFinish.append(self._startTimers)

        self.setStatus("Disconnected")

        log("OpenTunnel UI loaded")

    # -----------------------------------------
    # TIMERS
    # -----------------------------------------
    def _startTimers(self):

        self._pollTimer = eTimer()
        self._pollTimer.callback.append(self._pollMessages)
        self._pollTimer.start(POLL_MS, True)

        self._monitorTimer = eTimer()
        self._monitorTimer.callback.append(self._monitorTick)
        self._monitorTimer.start(MONITOR_MS, True)

        log("UI timers started")

        # Auto connect if enabled
        try:
            if config.plugins.opentunnel.autoconnect.value:
                self.toggleTunnel()
        except Exception as e:
            log("Auto connect error: %s" % e)

    def _pollMessages(self):

        try:
            while True:
                msg = self.ssh.poll_message()
                if msg is None:
                    break
                self._handleSshMessage(msg)
        except Exception as e:
            log("Poll error: %s" % e)

        if not self.closing and hasattr(self, "_pollTimer"):
            self._pollTimer.start(POLL_MS, True)

    def _monitorTick(self):

        try:
            running = self.ssh.is_running()
            now = time.time()

            # Blue button
            if self.busy_action in ("connect", "disconnect") or self.ssh.is_connecting():
                self["key_blue"].setText("Please wait...")
            else:
                self["key_blue"].setText("Disconnect" if running else "Connect")

            # Yellow button
            if self.busy_action == "test":
                self["key_yellow"].setText("Please wait...")
            else:
                self["key_yellow"].setText("Test")

            # وقتی عملیات در حال انجام است status را دست نزن
            if self.busy_action is None and now >= self._status_hold_until:
                self.setStatus("Connected" if running else "Disconnected")

        except Exception as e:
            log("Monitor error: %s" % e)

        if not self.closing and hasattr(self, "_monitorTimer"):
            self._monitorTimer.start(MONITOR_MS, True)

    # -----------------------------------------
    # SSH MESSAGES
    # -----------------------------------------
    def _handleSshMessage(self, msg):

        kind, text = msg

        if kind == MSG_CONNECTED:
            self.busy_action = None
            self["key_blue"].setText("Disconnect")
            self.setStatus("Connected")
            log("Connect result: %s" % text)

        elif kind == MSG_FAILED:
            self.busy_action = None
            self["key_blue"].setText("Connect")
            self.setStatus(self._shortConnectError(text), STATUS_HOLD_MS)
            log("Connect failed: %s" % text)

        elif kind == MSG_DISCONNECTED:
            was_busy = self.busy_action
            self.busy_action = None
            self["key_blue"].setText("Connect")

            if text == "Disconnected by user" or was_busy == "disconnect":
                self.setStatus("Disconnected")
            else:
                self.setStatus("Tunnel Lost", STATUS_HOLD_MS)

            log("Disconnect event: %s" % text)

        elif kind == MSG_TEST_OK:
            self.busy_action = None
            self["key_yellow"].setText("Test")
            self.setStatus("SSH OK", STATUS_HOLD_MS)
            log("Test OK: %s" % text)

        elif kind == MSG_TEST_FAIL:
            self.busy_action = None
            self["key_yellow"].setText("Test")
            self.setStatus(self._shortTestError(text), STATUS_HOLD_MS)
            log("Test failed: %s" % text)

    # -----------------------------------------
    # STATUS
    # -----------------------------------------
    def setStatus(self, text, hold_ms=0):

        if text != self._status_text:
            self._status_text = text
            self["status"].setText(text)
            log("STATUS: %s" % text)

        if hold_ms > 0:
            self._status_hold_until = time.time() + (float(hold_ms) / 1000.0)
        else:
            if text in ("Connected", "Disconnected"):
                self._status_hold_until = 0

    def _shortConnectError(self, msg):
        if msg == "sshpass is not installed":
            return "sshpass missing"
        if msg in ("Already connecting", "Disconnect in progress", "Already connected"):
            return msg
        return "Connection Failed"

    def _shortTestError(self, msg):
        if msg == "sshpass is not installed":
            return "sshpass missing"
        if msg in ("Test already in progress", "Client is busy", "Connection timeout"):
            return msg
        return "Test Failed"

    def _getSocksPort(self):
        try:
            return config.plugins.opentunnel.socks_port.value
        except Exception:
            return 1080

    # -----------------------------------------
    # TEST
    # -----------------------------------------
    def testConnection(self):

        if self.closing:
            return

        if self.busy_action is not None:
            log("Test ignored - busy: %s" % self.busy_action)
            return

        self.busy_action = "test"
        self["key_yellow"].setText("Please wait...")
        self.setStatus("Testing SSH...")

        started = self.ssh.test(
            config.plugins.opentunnel.server.value,
            config.plugins.opentunnel.port.value,
            config.plugins.opentunnel.username.value,
            config.plugins.opentunnel.password.value,
        )

        # اگر به هر دلیل شروع نشد، event خیلی زود از صف می‌آید.
        # اینجا کاری نمی‌کنیم تا UI از همان event نتیجه بگیرد.
        if not started:
            log("Test did not start immediately")

    # -----------------------------------------
    # CONNECT / DISCONNECT
    # -----------------------------------------
    def toggleTunnel(self):

        if self.closing:
            return

        if self.busy_action is not None:
            log("Toggle ignored - busy: %s" % self.busy_action)
            return

        # Disconnect — کاملاً event-based
        if self.ssh.is_running():
            self.busy_action = "disconnect"
            self["key_blue"].setText("Please wait...")
            self.setStatus("Disconnecting...")

            started = self.ssh.disconnect()
            if not started:
                self.busy_action = None
                self["key_blue"].setText("Connect")
                self.setStatus("Disconnected")
            return

        # Connect
        self.busy_action = "connect"
        self["key_blue"].setText("Please wait...")
        self.setStatus("Connecting...")

        started = self.ssh.connect(
            config.plugins.opentunnel.server.value,
            config.plugins.opentunnel.port.value,
            config.plugins.opentunnel.username.value,
            config.plugins.opentunnel.password.value,
            self._getSocksPort(),
        )

        # اگر connect واقعاً شروع نشود، event خطا از ssh.py می‌آید
        if not started:
            log("Connect did not start immediately")

    # -----------------------------------------
    # SAVE
    # -----------------------------------------
    def save(self):

        for item in self["config"].list:
            item[1].save()

        try:
            configfile.save()
        except Exception as e:
            log("Config save error: %s" % e)

        self.setStatus("Saved", 1000)
        self.close()

    # -----------------------------------------
    # CANCEL
    # -----------------------------------------
    def cancel(self):

        for item in self["config"].list:
            item[1].cancel()

        self.close()

    # -----------------------------------------
    # CLEANUP
    # -----------------------------------------
    def cleanup(self):

        self.closing = True

        if hasattr(self, "_pollTimer"):
            try:
                self._pollTimer.stop()
            except Exception:
                pass

        if hasattr(self, "_monitorTimer"):
            try:
                self._monitorTimer.stop()
            except Exception:
                pass

        try:
            self.ssh.disconnect(notify=False)
        except Exception as e:
            log("Cleanup disconnect error: %s" % e)

        log("Cleanup finished")