PIP_COMPILE_ARGS := --generate-hashes --no-header --verbose

.PHONY: compile-requirements
compile-requirements:
	pip-compile $(PIP_COMPILE_ARGS) requirements.in
	test -f requirements.local.in && pip-compile $(PIP_COMPILE_ARGS) requirements.local.in || exit 0

.PHONY: sync-requirements
sync-requirements:
	pip install pip-tools
	pip-sync requirements.txt requirements.*.txt
