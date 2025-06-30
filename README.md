Simple WIFI Simulator Toolkit

Under Development

This Code Support Plugins 😊😊😊 



# 🚀 Wifi Hack Simulator Toolkit

A **modular and safe Wi‑Fi attack simulator** designed for educational and ethical hacking purposes. Ideal for students, security enthusiasts, and ethical hackers who want to learn hands-on without targeting real networks.

---

## 🎯 Key Features

- Simulates attacks against different Wi‑Fi security types: **WEP**, **WPA/WPA2**, **WPS**, and supports **handshake capture**
- Includes ready-to-use attack modules:
  - Deauthentication Attack
  - Fake AP (Evil Twin)
  - Wordlist Brute‑Force
  - And more…
- **Automatic reporting** of results (e.g., handshake detection, crack success)
- Fully modular and extendable with a clean, plugin-style architecture

---

## 🛠️ Requirements & Installation

Designed to run in a **monitor-mode-capable environment** (Debian/Kali recommended):

```bash
sudo apt update
sudo apt install python3 python3-venv git
git clone https://github.com/ysnrfd/wifi-hack-simulator-toolkit.git
cd wifi-hack-simulator-toolkit
python3 -m venv venv
source venv/bin/activate
