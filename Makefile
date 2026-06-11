# ============================================
# OSINT TOOLKIT - Makefile pour Windows
# Compatible avec cmd.exe et PowerShell
# ============================================

# Configuration
PYTHON = python
APP = app.py
PORT = 5000

# Cible par défaut
.DEFAULT_GOAL := help

# Aide
.PHONY: help
help:
	@echo ============================================================
	@echo   [?] OSINT TOOLKIT - Commandes disponibles
	@echo ============================================================
	@echo   [+] make run      - Run OSINT Toolkit
	@echo   [+] make install  - Install dependencies
	@echo   [+] make clean    - Clean cache files
	@echo   [+] make update   - Update requirements.txt
	@echo   [+] make dev      - Development mode
	@echo   [+] make start    - Install and start
	@echo   [+] make fresh    - Clean and start
	@echo   [+] make help     - Display this help message
	@echo ============================================================

# Démarrer l'application
.PHONY: run
run:
	@echo  Running OSINT Toolkit...
	@echo  http://127.0.0.1:%PORT%
	@echo ============================================================
	@$(PYTHON) $(APP)

# Installer les dépendances
.PHONY: install
install:
	@echo [*] Installing dependencies...
	@pip install -r requirements.txt
	@echo [*] Dependencies installed!

# Nettoyer les fichiers cache
.PHONY: clean
clean:
	@echo [*] Cleaning cache files...
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist templates\__pycache__ rmdir /s /q templates\__pycache__
	@del /q *.pyc 2>nul
	@echo [*] Cleaning completed!

# Mettre à jour requirements.txt
.PHONY: update
update:
	@echo [*] Updating requirements.txt...
	@pip freeze > requirements.txt
	@echo [*] requirements.txt updated!

# Mode développement
.PHONY: dev
dev:
	@echo [*] 🐛 Mode développement...
	@set FLASK_ENV=development && set FLASK_DEBUG=1 && $(PYTHON) $(APP)

# Installer et démarrer
.PHONY: start
start: install run

# Nettoyer et démarrer
.PHONY: fresh
fresh: clean run
