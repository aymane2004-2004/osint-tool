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
	@echo 🔍 OSINT TOOLKIT - Commandes disponibles
	@echo ============================================================
	@echo   [+] make run      - Démarrer l'application
	@echo   [+] make install  - Installer les dépendances
	@echo   [+] make clean    - Supprimer les fichiers cache
	@echo   [+] make update   - Mettre à jour requirements.txt
	@echo   [+] make dev      - Mode développement
	@echo   [+] make start    - Installer + Démarrer
	@echo   [+] make fresh    - Nettoyer + Démarrer
	@echo   [+] make help     - Afficher cette aide
	@echo ============================================================

# Démarrer l'application
.PHONY: run
run:
	@echo 🚀 Démarrage de OSINT Toolkit...
	@echo 📍 http://127.0.0.1:%PORT%
	@echo ============================================================
	@$(PYTHON) $(APP)

# Installer les dépendances
.PHONY: install
install:
	@echo 📦 Installation des dépendances...
	@pip install -r requirements.txt
	@echo ✅ Installation terminée!

# Nettoyer les fichiers cache
.PHONY: clean
clean:
	@echo 🧹 Nettoyage du cache...
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist templates\__pycache__ rmdir /s /q templates\__pycache__
	@del /q *.pyc 2>nul
	@echo ✅ Nettoyage terminé!

# Mettre à jour requirements.txt
.PHONY: update
update:
	@echo 📝 Mise à jour de requirements.txt...
	@pip freeze > requirements.txt
	@echo ✅ requirements.txt mis à jour!

# Mode développement
.PHONY: dev
dev:
	@echo 🐛 Mode développement...
	@set FLASK_ENV=development && set FLASK_DEBUG=1 && $(PYTHON) $(APP)

# Installer et démarrer
.PHONY: start
start: install run

# Nettoyer et démarrer
.PHONY: fresh
fresh: clean run