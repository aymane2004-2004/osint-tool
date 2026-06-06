<div align="center">

# 🕵️ OSINT Analyzer Ultimate

**Advanced Open-Source Intelligence Gathering Platform**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)
![Playwright](https://img.shields.io/badge/Playwright-latest-green?style=for-the-badge&logo=playwright)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

> Automate digital footprint discovery, source classification, and intelligence visualization — all from a single search query.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Makefile Commands](#-makefile-commands)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🔍 Overview

**OSINT Analyzer Ultimate** is a web-based intelligence-gathering platform that automates the collection, classification, and visualization of publicly available information. Given any search query — a name, company, domain, or keyword — the tool uses a headless browser to extract results from DuckDuckGo, classifies each source by type, and renders an interactive node graph mapping the digital footprint.

Built for cybersecurity researchers, journalists, and digital investigators who need structured intelligence fast.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔎 **Headless Scraping** | Uses Playwright to simulate a real browser and bypass bot detection |
| 🧹 **URL Cleaning** | Unwraps all DuckDuckGo redirect formats and validates URLs |
| 🏷️ **Auto Classification** | Categorizes sources — social media, news, government, educational, and more |
| 🕸️ **Graph Visualization** | Interactive node map built with vis-network showing source relationships |
| 🖼️ **Live Favicons** | Displays each website's real favicon using Google's favicon service |
| 📋 **One-Click Actions** | Visit or copy any URL directly from the results panel |
| ⚡ **Asset Blocking** | Blocks images, fonts, and stylesheets during scraping for maximum speed |

---

## 🛠️ Tech Stack

**Backend**
- [Python 3.8+](https://www.python.org/) — core language
- [Flask](https://flask.palletsprojects.com/) — lightweight web framework
- [Playwright](https://playwright.dev/python/) — headless browser automation

**Frontend**
- [vis-network](https://visjs.github.io/vis-network/) — interactive graph visualization
- [Bootstrap 5](https://getbootstrap.com/) — responsive UI framework
- [Font Awesome 6](https://fontawesome.com/) — iconography
- Vanilla JavaScript — zero frontend framework overhead

---

## ⚙️ Prerequisites

- Python **3.8** or higher
- pip (Python package manager)
- Git
- Windows / Linux / macOS

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/osint-analyzer-ultimate.git
cd osint-analyzer-ultimate
```

### 2. Install dependencies

```bash
make install
```

Or manually:

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Run the application

```bash
make run
```

Then open your browser at:

```
http://127.0.0.1:5000
```

---

## 🖥️ Usage

1. Enter any search query in the terminal-style input field (name, company, domain, keyword, etc.)
2. Select the analysis depth (Basic / Standard / Deep)
3. Click **EXEC** and wait for the intelligence extraction to complete
4. Explore results in the **interactive graph** or the **URL log panel**
5. Use **VISIT** to open a source or **COPY** to copy its URL

---

## 📁 Project Structure

```
osint-analyzer-ultimate/
│
├── app.py                  # Flask backend — scraping, cleaning, classification
├── requirements.txt        # Python dependencies
├── Makefile                # Build and run commands
│
└── templates/
    └── index.html          # Frontend — graph, results panel, UI
```

---

## ⚙️ How It Works

```
User Query
    │
    ▼
Playwright (headless Chromium)
    │  → navigates DuckDuckGo
    │  → waits for result selectors
    │  → blocks images/fonts for speed
    │
    ▼
URL Extraction & Cleaning
    │  → unwraps DDG redirect URLs (/l/?uddg=...)
    │  → validates and deduplicates
    │
    ▼
Source Classification
    │  → social media, news, government, educational...
    │  → based on domain pattern matching
    │
    ▼
JSON Response to Frontend
    │
    ▼
vis-network Graph + Results Panel
    │  → nodes colored by source type
    │  → favicons loaded per domain
    │  → clickable nodes open URLs
```

---

## 📦 Makefile Commands

| Command | Description |
|---|---|
| `make run` | Start the OSINT Toolkit |
| `make install` | Install all dependencies |
| `make clean` | Remove cache files (`__pycache__`, `.pyc`) |
| `make update` | Regenerate `requirements.txt` from current environment |
| `make dev` | Run in Flask development mode with debug enabled |
| `make start` | Install dependencies then start the app |
| `make fresh` | Clean cache then start the app |
| `make help` | Display all available commands |

---

## ⚠️ Disclaimer

This tool is intended **strictly for educational purposes and authorized security research**. It only collects publicly available information indexed by search engines. The user is solely responsible for ensuring their use of this tool complies with applicable laws and the terms of service of any platform queried.

**Do not use this tool to:**
- Target individuals without their consent
- Violate any platform's terms of service
- Engage in any illegal surveillance or harassment

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ for the cybersecurity community

⭐ Star this repo if you find it useful!

</div>