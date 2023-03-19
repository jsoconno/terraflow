VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
TERRAFLOW_FILES = ./terraflow/**/*.py

.PHONY: help install install-dev test clean build dist lint run hooks document

help:
	@echo "Available targets:"
	@echo "  help        Show this help"
	@echo "  run         Create a virtual environment and show instructions"
	@echo "  hooks       Set up git hooks"
	@echo "  install-dev Install the CLI application in editable mode with development dependencies"
	@echo "  test        Run tests"
	@echo "  document    Generate documentation"
	@echo "  clean       Clean up build artifacts and temporary files"
	@echo "  build       Build the CLI application"
	@echo "  dist        Package the CLI application for distribution"
	@echo "  lint        Run linting checks on the codebase"

run: $(VENV)/bin/activate
	@echo "\nYour python virtual environment is ready!  To activate it, run the following command:\n\n- source $(VENV)/bin/activate"
	@echo "\nTo install the latest cli, run:\n\n- make install-dev\n"
	@echo "Happy coding!"

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

hooks:
	git config core.hooksPath .githooks

install-dev:
	$(PIP) install -e .[dev]

test:
	$(PYTHON) -m pytest

document:
	$(PYTHON) auto-generate-docs.py

build: clean
	$(PYTHON) setup.py build

dist: clean
	$(PYTHON) setup.py sdist bdist_wheel

lint:
	$(PYTHON) -m flake8
	$(PYTHON) -m black --check .
	$(PYTHON) -m mypy .

black:
	$(PYTHON) -m black .

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf build dist *.egg-info
