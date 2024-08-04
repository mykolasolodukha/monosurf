ifneq ("$(wildcard .env)","")
include .env
endif


COMMIT_MSG_TEMPLATE = ":bookmark: Release \`v{version}\`"


SOURCES_DIR = "./monosurf"

.PHONY: env
env:
	poetry install



.PHONY: commit_version
commit_version:
	@{ \
		git add pyproject.toml; \
		VERSION=$$(poetry version | cut -d' ' -f2); \
		COMMIT_MSG=$$(echo $(COMMIT_MSG_TEMPLATE) | sed "s/{version}/$${VERSION}/g"); \
		echo "Bumped version: $${VERSION}"; \
		echo "Generated Commit Message: $${COMMIT_MSG}"; \
		git commit -m "$${COMMIT_MSG}" -- pyproject.toml; \
		git tag "v$${VERSION}"; \
	}

.PHONY: bump-major
bump-major:
	poetry version major
	$(MAKE) commit_version

.PHONY: bump-minor
bump-minor:
	poetry version minor
	$(MAKE) commit_version

.PHONY: bump-patch
bump-patch:
	poetry version patch
	$(MAKE) commit_version


.PHONY: setup
setup:
# Echo the command to be executed, with some information about the command itself.
	echo "Creating virtual environment and installing dependencies..."
	make env


.PHONY: style
style:
	poetry run black $(SOURCES_DIR)
	poetry run isort $(SOURCES_DIR)
	poetry run pylint $(SOURCES_DIR)
	poetry run pydocstyle $(SOURCES_DIR)