# ama-hoi
REST API for coordinating employees and available work stations in office buildings.
For full API documentation check out our [swagger documentation](https://y7415815dh.execute-api.eu-west-1.amazonaws.com/prod/api/openapi)


### Setup developer environment

Set up local python environment:

This service uses python 3.8. If you do not have python 3.8 on your computer we can recommend using [pyenv](https://github.com/pyenv/pyenv) in order to install and use it.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pip-tools
pip install black
```

Install node packages and set up build environment:
```
make init
```

### Add new python packages to build environment:

To install new python packages add it to `setup.py => install_requires` then run `pip-compile` => `pip install -r requirements.txt`

### Running tests

Tests are run using [tox](https://pypi.org/project/tox/)

To run test with our python build environment: `make test`

To run auto format: `make format` 

For tests and linting we use [pytest](https://pypi.org/project/pytest/),
[flake8](https://pypi.org/project/flake8/) and
[black](https://pypi.org/project/black/).


### Running the application locally

This api uses FastAPI web framework. To run the application locally: `uvicorn app.main:app --host 0.0.0.0 --port 8000`


### Deploy

This Service uses serverless framework for deploying lambda functions. For ease of use we have contained the serverless deploy command in
our makefile. In order to deploy simply run:
```
make login
make deploy
```

### Infrastructure

Our infrastructure is setup using terraform. The terraform code can be found in the subdirectory `/terraform`
