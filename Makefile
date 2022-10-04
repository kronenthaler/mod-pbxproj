.PHONY: coverage test

coverage:
	cd tests; PYTHONPATH=../ pytest --cov-report=xml --cov=../pbxproj --cov-branch

coverage-term:
	cd tests; PYTHONPATH=../ pytest --cov-report=term --cov=../pbxproj --cov-branch

test:
	cd tests; PYTHONPATH=../ pytest
