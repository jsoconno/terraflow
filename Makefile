VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
TERRAFLOW_FILES = ./terraflow/**/*.py

run: $(VENV)/bin/activate
	@echo "\nYour python virtual environment is ready!  To activate it, run the following command:\n\n- source $(VENV)/bin/activate"
	@echo "\nTo install the latest cli, run:\n\n- make install\n"
	@echo "Happy coding!"

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

hooks:
	git config core.hooksPath .githooks

install:
	pip3 install --editable .

document:
	python3 auto-generate-docs.py

make lint:
	pylint $(TERRAFLOW_FILES)
	mypy $(TERRAFLOW_FILES)

make format:
	black $(TERRAFLOW_FILES)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)