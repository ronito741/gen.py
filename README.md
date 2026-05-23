# Wordlist Suite: Mutation Engine & Multi-Matrix Combiner

A lightweight, local graphical user interface (GUI) tool built in Python for modifying, expanding, and combining dictionary files and wordlists for security auditing, pattern analysis, and verification testing.

## Features
*   **Mutation Engine:** Expand base words with custom character matrices, complex symbol injections, and sequential anchor variations.
*   **Multi-Matrix Combiner:** Seamlessly join a primary file against a multi-file queue or manual comma-separated string entries using custom delimiter connections.

---

## 📋 System Requirements & Dependencies

The application relies entirely on standard Python core libraries and does not require third-party `pip` installations.

### 1. Windows & macOS
*   **Python 3.6 or newer**
*   *Note for Windows users:* Ensure the **"Add Python to PATH"** option is checked during installation so the system terminal recognizes the executable.

### 2. Linux (Kali Linux, Ubuntu, Debian)
Linux distributions package the graphical components separately. You must ensure the Python Tkinter package is installed manually.

---

## 🚀 Quick Start Guide

### Verification & Installation
Open your terminal or command prompt and run the following commands to check your environment and install missing components:

```bash
# 1. Verify Python installation
python3 --version

# 2. Linux Only: Install missing graphical dependencies (Kali/Ubuntu/Debian)
sudo apt update && sudo apt install python3-tk -y
