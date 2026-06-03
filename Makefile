# ============================================
# OSINT TOOLKIT - PowerShell Makefile
# Fast execution for Windows
# ============================================

# Configuration
PYTHON = python
APP = app.py
PORT = 5000

# Default target
.DEFAULT_GOAL := help

# Help command
.PHONY: help
help:
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor Cyan"
	@powershell -Command "Write-Host '🔍 OSINT TOOLKIT - Commands' -ForegroundColor Green"
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor Cyan"
	@powershell -Command "Write-Host '  make run      - Start the application' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make install  - Install dependencies' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make clean    - Remove cache files' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make update   - Update requirements.txt' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make dev      - Development mode' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make start    - Install + Run' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make fresh    - Clean + Run' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  make help     - Show this help' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor Cyan"

# Run the application (fast)
.PHONY: run
run:
	@powershell -Command "Write-Host '🚀 Starting OSINT Toolkit...' -ForegroundColor Green"
	@powershell -Command "Write-Host '📍 http://127.0.0.1:$(PORT)' -ForegroundColor Cyan"
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor DarkGray"
	@$(PYTHON) $(APP)

# Install dependencies
.PHONY: install
install:
	@powershell -Command "Write-Host '📦 Installing dependencies...' -ForegroundColor Yellow"
	@pip install -r requirements.txt
	@powershell -Command "if ($$?) { Write-Host '✅ Installation complete!' -ForegroundColor Green } else { Write-Host '❌ Installation failed!' -ForegroundColor Red }"

# Clean cache files (fast)
.PHONY: clean
clean:
	@powershell -Command "Write-Host '🧹 Cleaning cache...' -ForegroundColor Yellow"
	@powershell -Command "Get-ChildItem -Path . -Include '__pycache__' -Recurse -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
	@powershell -Command "Remove-Item -Path *.pyc -Force -ErrorAction SilentlyContinue"
	@powershell -Command "Write-Host '✅ Cleanup complete!' -ForegroundColor Green"

# Update requirements.txt
.PHONY: update
update:
	@powershell -Command "Write-Host '📝 Updating requirements.txt...' -ForegroundColor Yellow"
	@pip freeze > requirements.txt
	@powershell -Command "Write-Host '✅ requirements.txt updated!' -ForegroundColor Green"

# Development mode (with auto-reload)
.PHONY: dev
dev:
	@powershell -Command "Write-Host '🐛 Development mode...' -ForegroundColor Yellow"
	@powershell -Command "$$env:FLASK_ENV='development'; $$env:FLASK_DEBUG='1'"
	@$(PYTHON) $(APP)

# Install and run (one command)
.PHONY: start
start: install run

# Clean and run (one command)
.PHONY: fresh
fresh: clean run

# Show app info
.PHONY: info
info:
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor Cyan"
	@powershell -Command "Write-Host '📊 OSINT TOOLKIT Info' -ForegroundColor Green"
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor Cyan"
	@powershell -Command "Write-Host 'App:        $(APP)' -ForegroundColor White"
	@powershell -Command "Write-Host 'Port:       $(PORT)' -ForegroundColor White"
	@powershell -Command "Write-Host 'Python:     ' -NoNewline; python --version"
	@powershell -Command "Write-Host 'Files:      ' -NoNewline; (Get-ChildItem -Filter *.py).Count -ForegroundColor White"
	@powershell -Command "Write-Host '═══════════════════════════════════════════════════════════════' -ForegroundColor Cyan"

# Open browser
.PHONY: open
open:
	@powershell -Command "Start-Process 'http://127.0.0.1:$(PORT)'"
	@powershell -Command "Write-Host '✅ Browser opened!' -ForegroundColor Green"

# Run and open browser
.PHONY: launch
launch: run open