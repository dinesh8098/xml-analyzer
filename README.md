# 📊 XML Configuration Analyzer (Flask Web App)

A web-based XML analysis tool built with Flask that compares and validates configuration files (PAVAST, FS, and optional XDI data). It identifies mismatches, missing elements, tag inconsistencies, and SYSCOND deviations through an interactive dashboard.

---

## 🚀 Live Deployment

This application is deployed on **Render**.

👉 Live URL: `https://your-app-name.onrender.com`

---

## 🧠 Features

- Compare **PAVAST vs FS XML files**
- Detect missing elements in both directions
- Validate configuration tags:
  - SW-VARIABLE
  - SW-CALPRM
  - SW-SYSTEMCONST
  - MESSAGE types
- SYSCOND logic parsing and deviation detection
- Optional XDI metadata extraction
- Interactive dashboard with:
  - Summary statistics
  - Category-wise issue breakdown
  - Metadata viewer
- Modern responsive UI (HTML + CSS + JS)

---

## 🏗️ Tech Stack

- Python 3
- Flask
- XML Parsing (xml.etree.ElementTree)
- Jinja2 Templates
- HTML5, CSS3, JavaScript

---

## 📁 Project Structure
