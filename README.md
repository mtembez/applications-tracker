# ⚡ Applications Tracker (Lion Console)

[![CI Verification](https://github.com/mtembez/applications-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/mtembez/applications-tracker/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Zero-Slop](https://img.shields.io/badge/Design-Linear%20%26%20Vercel%20Grade-cyan.svg)]()

> High-precision, zero-latency job application tracker and telemetry pipeline designed for systems and software engineers. Built with a dual-interface architecture: a high-speed terminal CLI paired with an elite Linear/Vercel-grade multicolor web console featuring Magic UI aurora lighting and an ambient Celestial Lion constellation emblem.

---

## ✨ Features & Architecture

* **🎨 Linear & Vercel Aesthetic:** Monochromatic dark zinc/OLED canvas (`#000000`, `#09090b`) with vibrant multi-color accents (cyan, violet, fuchsia, amber, emerald) and Geist typography.
* **🦁 Celestial Lion Emblem:** Translucent geometric constellation Lion watermark layered behind the pipeline, engineered with native SVG vector paths and ambient breathing pulses.
* **🌌 Magic UI & Aceternity Animations:** 4-sphere ambient aurora mesh drift (`@keyframes aurora-drift`), shimmer text gradients, and glowing card borders with conic mask reflections.
* **⌘K Command Palette (`pacocoursey/cmdk`):** Press `⌘K` or `Ctrl+K` to search across all companies, filter stages, or execute actions instantly from the keyboard.
* **📋 Dual View Pipeline:** Seamless toggle between an interactive **Workflow Kanban Board** (with 1-click stage advancement buttons: `→ Screen`, `→ Tech`, `→ Offer`) and a **High-Density Data Table**.
* **🗂 Slide-Over Detail Drawer:** Click any application to open a sleek slide-over drawer with full properties, quick stage transitions, notes, and a chronological audit timeline.
* **⚡ WAL Concurrency & ACID Safety:** SQLite persistence engine running in Write-Ahead Logging (`PRAGMA journal_mode = WAL;`) with foreign key cascade guarantees and sub-millisecond query performance.
* **💻 High-Speed Terminal CLI (`apptracker`):** Full Rich-powered CLI for lightning-fast command-line interaction without leaving your terminal.

---

## 🚀 Quickstart

### 1. Local Setup

```bash
# Clone the repository
git clone https://github.com/mtembez/applications-tracker.git
cd applications-tracker

# Install minimal dependencies
pip install -r requirements.txt

# Launch the interactive web console
python3 -m tracker.server
# Open http://localhost:8765 in your browser
```

### 2. Using the CLI Tool (`apptracker`)

```bash
# Make executable and symlink globally
chmod +x apptracker
ln -s $(pwd)/apptracker ~/.local/bin/apptracker

# View the pipeline table
apptracker list

# Record a new opportunity
apptracker add -c "Microsoft ADC" -r "Systems Engineer" -l NAIROBI --compensation "KES 450,000" --channel "Referral"

# Transition status with audit feedback
apptracker status 1 TECHNICAL -m "Completed distributed systems whiteboarding"

# Inspect conversion metrics
apptracker metrics
```

---

## 🐳 Docker Deployment

Run self-contained in a hardened Linux container:

```bash
# Build Docker image
docker build -t applications-tracker .

# Run on port 8765 with persistent storage volume
docker run -d -p 8765:8765 -v $(pwd)/data:/app/data --name apptracker applications-tracker
```

---

## ☁️ 1-Click Cloud Deployment

### Deploy to Render
1. Fork or push this repository to your GitHub account (`mtembez/applications-tracker`).
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** $\to$ **Blueprint**, connect your repository, and select `render.yaml`.
4. Render will automatically provision the Python 3.13 web service with zero manual configuration.

---

## 🧪 Deterministic Verification Suite

The codebase enforces compiler-grounded verification across domain models, SQLite WAL operations, REST APIs, CLI commands, and UI contracts:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

```text
Ran 39 tests in 0.217s
OK (Exit Code 0)
```

---

## 📜 License

MIT License. Designed and engineered by [Simon Munyambu](https://github.com/mtembez).
