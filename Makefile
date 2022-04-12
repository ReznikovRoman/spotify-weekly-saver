PIP_COMPILE_ARGS := --generate-hashes --no-header --verbose --no-emit-index-url

.PHONY: compile-requirements
compile-requirements:
	pip install pip-tools
	pip-compile $(PIP_COMPILE_ARGS) requirements.in
	test -f requirements.local.in && pip-compile $(PIP_COMPILE_ARGS) requirements.local.in || exit 0

.PHONY: sync-requirements
sync-requirements:
	pip install pip-tools
	pip-sync requirements.txt requirements.*.txt

.PHONY: check
check:
	flake8
