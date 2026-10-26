.PHONY: setup update upgrade migrate-dev reset-dev revision ci format-check lint-check typecheck unit-test format lint fix

# location of the sqlite db used for local development
export DEV_DB_PATH ?= .dev/home/dev.db

########################################
# Setup
########################################

# For setting up the development environment. Installs the dependencies without upgrading them.
setup:
	uv sync --all-packages --group dev --frozen

# For when updating a new dependency. Updates the lock file to the latest versions.
update:
	uv sync --all-packages --group dev

# For upgrading all dependencies to their latest versions. Bumps all versions to latest.
upgrade:
	uv sync --all-packages --group dev --upgrade


########################################
# Dev
########################################
export DEV_DB_URL ?= sqlite+aiosqlite:///$(CURDIR)/$(DEV_DB_PATH)
ALEMBIC_CMD = uv run --no-sync alembic -c packages/lila-core/alembic.ini

# Apply all migrations to the dev database.
migrate-dev:
	$(ALEMBIC_CMD) upgrade head

# Removes and recreates the dev database
reset-dev:
	rm -f $(DEV_DB_PATH)
	$(MAKE) migrate-dev

# Creates a revision from the latest models.
#		make revision MSG="descriptive message"
revision:
ifndef MSG
	$(error MSG is required, e.g. make revision MSG="descriptive message")
endif
	$(ALEMBIC_CMD) revision --autogenerate -m "$(MSG)"

########################################
# Test
########################################

# Run unit tests. Defaults to every package.
#   make unit-test                                              # all packages
#   make unit-test PACKAGE=lila-core                            # one package
#   make unit-test FILE=packages/lila-core/tst/path/test_x.py   # one file (FILE wins over PACKAGE)
# Exit code 5 (no tests collected) is not treated as a failure.
unit-test:
	@printf '\n'
ifdef FILE
	uv run --no-sync pytest $(FILE)
else ifdef PACKAGE
	cd packages/$(PACKAGE) && uv run --no-sync pytest
else
	@for p in packages/*/; do \
		(cd $$p && uv run --no-sync pytest) || [ $$? -eq 5 ] || exit 1; \
	done
endif


########################################
# CI
########################################

# For running in CI: format check, lint check, typecheck and unit tests, without making changes.
ci: format-check lint-check typecheck unit-test

# For running in CI to block without making changes.
format-check:
	@printf '\n==================== 🔍 format-check ====================\n'
	uv run black --check .

# For running in CI to block without making changes.
lint-check:
	@printf '\n==================== 🔍 lint-check ====================\n'
	uv run ruff check .

# Run before commit. For making sure there are no type errors.
typecheck:
	@printf '\n==================== 🧐 typecheck ====================\n'
	uv run --no-sync basedpyright


# Run before commit. For formatting the code according to style guidelines.
format:
	@printf '\n==================== ✨ format ====================\n'
	uv run black .

# Run before commit. For fixing lint issues.
lint:
	@printf '\n==================== 🧹 lint ====================\n'
	uv run ruff check --fix .

# Run before commit. Formats and lints.
fix: format lint