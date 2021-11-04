.AWS_PROFILE := knowit-playground

GLOBAL_PY := python3
BUILD_VENV ?= .build_venv
BUILD_PY := $(BUILD_VENV)/bin/python

DEVOPS_VENV ?= .devops_venv
DEVOPS_PY := $(DEVOPS_VENV)/bin/python

.PHONY: init
init: node_modules $(BUILD_VENV) $(DEVOPS_VENV)

node_modules: package.json package-lock.json
	npm install

# Setup build environment
$(BUILD_VENV):
	$(GLOBAL_PY) -m venv $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U pip

# Setup envirtonment for devops scripts
$(DEVOPS_VENV):
	$(GLOBAL_PY) -m venv $(DEVOPS_VENV)
	$(BUILD_PY) -m pip install -U pip
	$(DEVOPS_PY) -m pip install boto3

.PHONY: format
format: $(BUILD_VENV)/bin/black
	$(BUILD_PY) -m black .

.PHONY: test
test: $(BUILD_VENV)/bin/tox
	$(BUILD_PY) -m tox -p auto -o

.PHONY: upgrade-deps
upgrade-deps: $(BUILD_VENV)/bin/pip-compile
	$(BUILD_VENV)/bin/pip-compile -U

.PHONY: deploy
deploy: init format test# login
	@echo "\nDeploying to stage: $${STAGE:-prod}\n"
	AWS_PROFILE=$(.AWS_PROFILE) sls deploy --stage $${STAGE:-prod}

.PHONY: undeploy
undeploy:# login
	@echo "\nUndeploying stage: $(STAGE)\n"
	sls remove --stage $(STAGE) --aws-profile $(.AWS_PROFILE)

.PHONY: login
login:
	aws sso login --profile=$(.AWS_PROFILE)
	$(DEVOPS_PY) -m devops.copy_credentials --aws-profile=$(.AWS_PROFILE)


###
# Python build dependencies
##

$(BUILD_VENV)/bin/pip-compile: $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U pip-tools

$(BUILD_VENV)/bin/%: $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U $*
