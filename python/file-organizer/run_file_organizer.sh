#!/bin/bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
PYTHON_BIN="$VENV_DIR/bin/python3"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if ! command_exists python3; then
    echo "Error: python3 is not available on this system. Please install Python 3 before running this script."
    exit 1
fi

ensure_virtualenv() {
    if [[ ! -d "$VENV_DIR" ]] || [[ ! -x "$PYTHON_BIN" ]]; then
        echo "Virtual environment not found. Creating one at $VENV_DIR ..."
        python3 -m venv "$VENV_DIR"
        echo "Virtual environment created."
    else
        echo "Virtual environment detected at $VENV_DIR."
    fi
}

install_requirements() {
    if [[ -f "$REQUIREMENTS_FILE" ]]; then
        echo "Installing dependencies from $REQUIREMENTS_FILE ..."
        "$PYTHON_BIN" -m pip install --upgrade pip >/dev/null
        "$PYTHON_BIN" -m pip install -r "$REQUIREMENTS_FILE"
        echo "Dependencies installed."
    else
        echo "No requirements.txt found. Skipping dependency installation."
    fi
}

run_application() {
    echo "Starting File Organizer..."
    "$PYTHON_BIN" "$PROJECT_ROOT/organize_files_in_dir.py"
}

ensure_virtualenv
install_requirements
run_application

