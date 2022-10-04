.PHONY: coverage coverage-term test

coverage:
	cd tests; pytest --cov-report=xml --cov=../ --cov-branch
	cd tests; rm -rf .coverage

coverage-term:
	cd tests; pytest --cov-report=term --cov=../ --cov-branch
	cd tests; rm -rf .coverage

test:
	cd tests; pytest