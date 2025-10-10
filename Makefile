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

commit-bump-version:
	git add pbxproj/__init__.py
	git commit -m "chore: bump version to $(shell python3 -c 'import pbxproj; print(pbxproj.__version__)')"
	git push

tag-release:
	git tag -f "$(shell python3 -c 'import pbxproj; print(pbxproj.__version__)')"
	git push origin master --tags
