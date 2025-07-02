# 🔓 FTP Brute-Force Cracker – Ethical Hacking Tool

## 🧠 Overview

This is a Python-based tool that simulates a **brute-force attack on FTP servers** using a dictionary of passwords. It helps cybersecurity learners understand how FTP services can be tested for weak credentials in controlled environments.

> ⚠️ For educational and ethical use only. Do **not** use this on systems without permission.

---

## 🚀 Features

- 📁 Reads and tests passwords from a wordlist
- 🔁 Attempts login using `ftplib.FTP()`
- ✅ Logs and displays valid credentials on success
- 🧵 Supports custom ports and clean error handling
- ⚡ Simple and efficient command-line interface

---

## 🛠️ Technologies Used

- Python 3.x
- `ftplib` – for FTP session handling
- `argparse` – for CLI argument parsing
- `os`, `time` – for optional delays and file handling

---

## 📦 Usage

```bash
python3 ftp_cracker.py -H victim_IP -u anonymous -P passwords.txt -p 21
