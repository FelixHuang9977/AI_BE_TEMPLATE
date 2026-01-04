
# Detection of OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif

.PHONY: setup start stop status clean help

help:
	@echo "Available commands (OS: $(DETECTED_OS))"
	@echo "  make setup   - Create venv and install requirements"
	@echo "  make start   - Start the service"
	@echo "  make stop    - Stop the service"
	@echo "  make status  - Check service status"
	@echo "  make clean   - Remove venv and temp files"

setup:
ifeq ($(DETECTED_OS),Windows)
	python -m venv .venv
	.venv\Scripts\pip install -r requirements.txt
else
	python3 -m venv .venv
	.venv/bin/pip3 install -r requirements.txt
endif

start:
ifeq ($(DETECTED_OS),Windows)
	@echo "Starting on Windows..."
	@start .venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
	@echo "Service started in new window."
else
	@echo "Installing and starting systemd service..."
	sudo cp ai_diagbe.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable ai_diagbe
	sudo systemctl restart ai_diagbe
	sleep 3; make status
endif

launch: start

stop:
ifeq ($(DETECTED_OS),Windows)
	@echo "Stopping service on port 9000..."
	@for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9000') do taskkill /f /pid %%a
else
	sudo systemctl stop ai_diagbe
endif

status:
ifeq ($(DETECTED_OS),Windows)
	@echo "Checking port 9000..."
	@netstat -aon | findstr :9000 || echo "Service not running"
else
	sudo systemctl status ai_diagbe
	sudo netstat -ntpav | grep 9000 || echo "\nERROR!\nCannot find 9000 port listening\n"
endif

clean:
ifeq ($(DETECTED_OS),Windows)
	- del /q .tmp.* scripts\.tmp.* >nul 2>&1
else
	- rm -f .tmp.* scripts/.tmp.* > /dev/null 2>&1
endif

test:
ifeq ($(DETECTED_OS),Windows)
	.venv\Scripts\pytest -v --show-capture=all tests/test_real_predefined_id.py
else
	.venv/bin/pytest -v --show-capture=all tests/test_real_predefined_id.py
endif