# -*- coding: utf-8 -*-

import os
import subprocess
import time
from threading import Thread, Event, Lock
from queue import Queue, Empty

from .logger import log


MSG_CONNECTED    = "connected"
MSG_FAILED       = "failed"
MSG_DISCONNECTED = "disconnected"
MSG_TEST_OK      = "test_ok"
MSG_TEST_FAIL    = "test_fail"


class SSHClient:

    def __init__(self):

        self._process = None
        self._lock = Lock()
        self._stop = Event()

        self._connecting = False
        self._disconnecting = False
        self._testing = False

        # برای Auto Reconnect
        self._host = None
        self._port = None
        self._user = None
        self._password = None
        self._socks_port = 1080

        # صف پیام thread -> main loop
        self.queue = Queue()

    # -----------------------------------------
    # INTERNAL HELPERS
    # -----------------------------------------
    def _check_sshpass(self):
        return os.path.exists("/usr/bin/sshpass")

    def _put(self, msg_type, text):
        self.queue.put((msg_type, text))

    def _decode(self, data):
        if not data:
            return ""
        if isinstance(data, bytes):
            return data.decode(errors="ignore").strip()
        return str(data).strip()

    def _read_stderr(self, process, default_msg=""):
        try:
            out, err = process.communicate(timeout=1)
            return self._decode(err) or self._decode(out) or default_msg
        except Exception:
            return default_msg

    def _terminate(self, process):
        if process is None:
            return

        if process.poll() is not None:
            return

        try:
            process.terminate()
            process.wait(timeout=3)
        except Exception:
            try:
                process.kill()
                process.wait(timeout=1)
            except Exception:
                pass

    def _process_alive_nolock(self):
        if self._process is None:
            return False

        if self._process.poll() is None:
            return True

        self._process = None
        return False

    # -----------------------------------------
    # PUBLIC: STATUS
    # -----------------------------------------
    def is_running(self):
        with self._lock:
            return self._process_alive_nolock()

    def is_connecting(self):
        with self._lock:
            return self._connecting

    def poll_message(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            return None

    # -----------------------------------------
    # TEST
    # -----------------------------------------
    def test(self, host, port, user, password):

        if not self._check_sshpass():
            self._put(MSG_TEST_FAIL, "sshpass is not installed")
            return False

        with self._lock:
            if self._testing:
                self._put(MSG_TEST_FAIL, "Test already in progress")
                return False

            if self._connecting or self._disconnecting:
                self._put(MSG_TEST_FAIL, "Client is busy")
                return False

            self._testing = True

        def run():
            try:
                cmd = [
                    "sshpass", "-p", password,
                    "ssh",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ConnectTimeout=10",
                    "-p", str(port),
                    "%s@%s" % (user, host),
                    "echo OK"
                ]

                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10
                )

                out = self._decode(result.stdout)
                err = self._decode(result.stderr)

                if result.returncode == 0 and "OK" in out:
                    self._put(MSG_TEST_OK, "SSH OK")
                else:
                    self._put(MSG_TEST_FAIL, err or out or "SSH test failed")

            except subprocess.TimeoutExpired:
                self._put(MSG_TEST_FAIL, "Connection timeout")
            except Exception as e:
                self._put(MSG_TEST_FAIL, str(e))
            finally:
                with self._lock:
                    self._testing = False

        Thread(target=run, daemon=True).start()
        return True

    # -----------------------------------------
    # CONNECT
    # -----------------------------------------
    def connect(self, host, port, user, password, socks_port=1080):

        if not self._check_sshpass():
            self._put(MSG_FAILED, "sshpass is not installed")
            return False

        with self._lock:
            if self._connecting:
                self._put(MSG_FAILED, "Already connecting")
                return False

            if self._disconnecting:
                self._put(MSG_FAILED, "Disconnect in progress")
                return False

            if self._process_alive_nolock():
                self._put(MSG_FAILED, "Already connected")
                return False

            self._connecting = True
            self._stop.clear()

            # ذخیره برای reconnect
            self._host = host
            self._port = port
            self._user = user
            self._password = password
            self._socks_port = socks_port

        def run():
            process = None

            try:
                cmd = [
                    "sshpass", "-p", password,
                    "ssh",
                    "-N",
                    "-D", str(socks_port),
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ExitOnForwardFailure=yes",
                    "-o", "ServerAliveInterval=15",
                    "-o", "ServerAliveCountMax=2",
                    "-o", "ConnectTimeout=10",
                    "-p", str(port),
                    "%s@%s" % (user, host)
                ]

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE
                )

                with self._lock:
                    self._process = process

                time.sleep(1.5)

                if self._stop.is_set():
                    self._terminate(process)

                    with self._lock:
                        if self._process is process:
                            self._process = None
                        self._connecting = False

                    log("Connect aborted")
                    return

                if process.poll() is not None:
                    msg = self._read_stderr(process, "SSH exited immediately")

                    with self._lock:
                        if self._process is process:
                            self._process = None
                        self._connecting = False

                    self._put(MSG_FAILED, msg)
                    return

                with self._lock:
                    self._connecting = False

                log("Tunnel started")
                self._put(MSG_CONNECTED, "Tunnel started")

                self._watch(process)

            except Exception as e:
                with self._lock:
                    if self._process is process:
                        self._process = None
                    self._connecting = False

                self._put(MSG_FAILED, str(e))

        Thread(target=run, daemon=True).start()
        return True

    # -----------------------------------------
    # RECONNECT
    # -----------------------------------------
    def reconnect(self):

        with self._lock:
            host = self._host
            port = self._port
            user = self._user
            password = self._password
            socks_port = self._socks_port

        if not host or not user:
            self._put(MSG_FAILED, "No saved connection info")
            return False

        log("Reconnecting to %s@%s:%s" % (user, host, port))
        return self.connect(host, port, user, password, socks_port)

    # -----------------------------------------
    # WATCH
    # -----------------------------------------
    def _watch(self, process):

        while not self._stop.is_set():
            time.sleep(2)

            if self._stop.is_set():
                break

            if process is None:
                break

            if process.poll() is not None:

                if self._stop.is_set():
                    break

                msg = self._read_stderr(process, "Tunnel disconnected")

                with self._lock:
                    if self._process is process:
                        self._process = None

                    self._connecting = False
                    self._disconnecting = False

                log("Tunnel dropped: %s" % msg)
                self._put(MSG_DISCONNECTED, msg)
                break

    # -----------------------------------------
    # DISCONNECT
    # -----------------------------------------
    def disconnect(self, notify=True):

        with self._lock:
            alive = self._process_alive_nolock()

            if self._disconnecting:
                return False

            if not alive and not self._connecting:
                return False

            self._disconnecting = True
            self._stop.set()
            process = self._process
            self._process = None
            self._connecting = False

        def run():
            try:
                if process and process.poll() is None:
                    self._terminate(process)
            finally:
                with self._lock:
                    self._disconnecting = False

                log("Tunnel stopped by user")

                if notify:
                    self._put(MSG_DISCONNECTED, "Disconnected by user")

        Thread(target=run, daemon=True).start()
        return True