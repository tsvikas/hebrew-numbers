default:
  @just --list

# Initialize a new project
init:
  git init
  git commit --allow-empty -m "Initial commit"
  git add --all
  git commit -m "🚀 Initialized project using https://github.com/tsvikas/python-template"
  @just update-deps
  git add --all
  git commit -m "⬆️ Updated project dependencies"
  @just prepare

# Update all dependencies
update-deps:
  uv sync --upgrade
  uv run pre-commit autoupdate -j "$(nproc)"

# Initialize the project after cloning
prepare:
  uv run pre-commit install

# Run code quality checks, than push
check-and-push:
  @just check
  git push

# Format and check code
format-and-check:
  @just format
  @just check

# Run all code quality checks and tests
check:
  # only pytest and mypy are not in the pre-commit hooks
  uv run pytest
  uv run mypy
  uv run pre-commit run --all-files

format:
  uv run ruff check --select I001 --fix
  uv run black .
  uv run pre-commit run --all-files blacken-docs
  uv run pre-commit run --all-files mdformat

lint:
  uv run ruff check
  uv run mypy

test:
  uv run pytest
