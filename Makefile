.PHONY: coverage coverage-term test install-dependencies

coverage: install-dependencies
	cd tests; pytest --cov-report=xml --cov=../ --cov-branch
	cd tests; rm -rf .coverage

coverage-term: install-dependencies
	cd tests; pytest --cov-report=term --cov=../ --cov-branch
	cd tests; rm -rf .coverage

test:
	cd tests; pytest

install-dependencies:
	pip3 install -r dev-requirements.txt
