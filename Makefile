.PHONY: setup update upgrade ci format-check format typecheck unit-test

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
# CI
########################################

# For running in CI: format check, typecheck and unit tests, without making changes.
ci: format-check typecheck unit-test

# For running in CI to block without making changes.
format-check:
	@printf '\n==================== 🔍 format-check ====================\n'
	uv run black --check .
	uv run ruff check --select I .

# Run before commit. For formatting the code according to style guidelines.
format:
	@printf '\n==================== ✨ format ====================\n'
	uv run black .
	uv run ruff check --select I --fix .

# Run before commit. For making sure there are no type errors.
typecheck:
	@printf '\n==================== 🧐 typecheck ====================\n'
	uv run --no-sync basedpyright


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
