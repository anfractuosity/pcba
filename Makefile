SHELL := /bin/bash

install:
	python3 -m venv --system-site-packages env
	source ./env/bin/activate; pip install .
