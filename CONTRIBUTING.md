# Contributing

Do you want to fix an issue yourself? Great! some house rules:

1. Provide a description of what problem you are solving, what case was not being taking into account
2. Provide unit tests for the case you have fixed. Pull request without unit test or PRs that decrease the coverage will not be approved until this changes.
3. Adhere to the coding style and conventions of the project, for instance, target_name is used to specify the target across all functions that use this parameter. Changes will be requested on PRs that don't follow this.
4. Write descriptive commit messages.

### Getting Started
Create virtual environment.
```shell
virtualenv -p python3 .venv
```

Activate the environment.
```shell
source .venv/bin/activate
```

Install development dependencies.
```shell
pip install -r dev-requirements.txt
```

Run tests.
```shell
pytest --cov-report=term --cov=../ --cov-branch tests
```
