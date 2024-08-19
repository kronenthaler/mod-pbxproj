.PHONY: coverage coverage-term test install-dependencies

coverage: install-dependencies
	pytest --cov-report=xml --cov=../ --cov-branch
	rm -rf .coverage

coverage-term: install-dependencies
	pytest --cov-report=term --cov=../ --cov-branch
	rm -rf .coverage

test:
	pytest

install-dependencies:
	pip3 install -r dev-requirements.txt
