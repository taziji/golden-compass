.PHONY: install dev-install lint format test run-local

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -e .[dev]

lint:
	ruff golden_compass app

format:
	ruff --fix golden_compass app

mypy:
	mypy golden_compass

test:
	pytest

run-local:
	streamlit run app/main.py
