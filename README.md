# 🚀 MONZ XTER OTP SPAMMER

**Premium OTP Spammer with 25+ WhatsApp APIs**

## 📌 About

Professional OTP spammer tool with multi-API support.

## ✨ Features

- 🎯 **25+ APIs** - OTP WhatsApp spammer
- 🔐 **License System** - Trial + Premium
- 🖥️ **Multi-Platform** - Linux & Android (Termux)
- ⚡ **Multi-Threading** - 1-10 threads
- 🔄 **Auto Retry** - Retry failed requests

## 🛠️ Installation

### Termux (Android)

```bash
pkg update && pkg upgrade
termux-setup-storage
pkg install python git -y
git clone https://github.com/Flutter775/SpamOtp.git
cd SpamOtp
pip install -r requirements.txt
python main.py
```

### Linux

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/Flutter775/SpamOtp.git
cd SpamOtp
pip3 install -r requirements.txt
python3 main.py
```

## 📁 Structure

```
SpamOtp/
├── main.py              # Entry point
├── main_engine.py       # Attack engine
├── handlers_plain.py    # 25+ API handlers
├── license.py           # License system
├── utils.py             # Utilities
├── useragents.py        # UA list
├── targets.py           # Target list
├── config.py            # Config
├── requirements.txt     # Dependencies
└── README.md
```

## ⚠️ Disclaimer

This tool is for educational purposes only. Use at your own risk.
