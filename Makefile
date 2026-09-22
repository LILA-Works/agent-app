.PHONY: setup update upgrade format-check format typecheck

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

# For running in CI to block without making changes.
format-check:
	uv run black --check .
	uv run ruff check --select I .

# Run before commit. For formatting the code according to style guidelines.
format:
	uv run black .
	uv run ruff check --select I --fix .

# Run before commit. For making sure there are no type errors.
typecheck:
	uv run --no-sync basedpyright
