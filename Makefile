.PHONY: coverage coverage-term test

coverage:
	cd tests; pytest --cov-report=xml --cov=../pbxproj --cov-branch;
	cd tests; rm -rf .coverage

coverage-term:
	cd tests; pytest --cov-report=term --cov=../pbxproj --cov-branch;
	cd tests; rm -rf .coverage

test:
	cd tests; pytest