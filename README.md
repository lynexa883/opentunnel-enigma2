# OpenTunnel - Enigma2 SSH Tunnel Manager

OpenTunnel is a plugin for Enigma2 (OpenATV / OpenPLi / OpenViX) that allows full system traffic tunneling through SSH.

## 🚀 Features

- SSH connection with username/password
- One-click Connect / Disconnect
- Full system traffic tunneling (YouTube, IPTV, plugins, downloads)
- Auto-connect on boot
- Kill switch support (optional)
- Lightweight and fast
- Works on multiple architectures (ARM / ARM64 / MIPS / x86)

---

## 📺 Supported Receivers

- Vu+ series
- Dreambox
- Zgemma
- Octagon
- Edision
- Any Enigma2-based receiver

---

## ⚙️ Requirements

- OpenATV 7.6 or 8.x
- Python 3 (Enigma2)
- Root access on receiver
- SSH server account

---

## 📦 Installation

1. Copy plugin to:
/usr/lib/enigma2/python/Plugins/Extensions/OpenTunnel/

2. Restart Enigma2:
systemctl restart enigma2

or reboot device

---

## 🔌 How it works

OpenTunnel creates a secure SSH tunnel and routes all system traffic through it using tun2socks and routing rules.

---

## 🧠 Architecture

- Enigma2 GUI (Python)
- SSH Client
- SOCKS5 Proxy
- tun2socks engine
- Routing manager (iptables)
- DNS handler

---

## ⚠️ Disclaimer

This project is for educational purposes only. Users are responsible for how they use it.

---

## 👨‍💻 Development

Project is under active development.

Planned features:
- Multi-server support
- WireGuard support
- Auto reconnect
- Speed test
- Traffic stats

---

## 📜 License
