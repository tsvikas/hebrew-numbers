# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for converting numbers to Hebrew text representation. It handles the complex rules of Hebrew number grammar including gender, definiteness, and construct state.

### Key Functions

- `indefinite_number(n)`: General counting without specific nouns
- `ordinal_number(n, gender)`: Position in series (1st, 2nd, etc.)
- `cardinal_number(n, gender, construct)`: Basic number with gender and construct state
- `count_noun(n, singular, plural, gender, definite)`: Full noun counting with proper grammar
- `count_prefix(n, gender, definite)`: Just the numerical prefix

## Development Commands

### Essential Commands

- `uv run just test` - Run pytest tests
- `uv run just lint` - Run ruff and mypy linting
- `uv run just format` - Format code with black and ruff
- `uv run just check` - Run all quality checks (test + lint + pre-commit)

### Individual Tools

- `uv run pytest` - Run tests directly
- `uv run mypy` - Type checking
- `uv run ruff check` - Linting
- `uv run black .` - Code formatting
- `uv run pre-commit run --all-files` - All pre-commit hooks

### Setup

- `uv run just prepare` - Setup development environment (run after cloning)

## Project Structure

### Core Code

- `src/hebrew_numbers/__init__.py` - Main API exports
- `src/hebrew_numbers/hebrew_numbers.py` - Core implementation
- `tests/` - Test files

### Configuration

- Uses `uv` for dependency management
- `pyproject.toml` - Project configuration, dependencies, and tool settings
- `justfile` - Task runner (like Makefile)
- `.pre-commit-config.yaml` - Extensive pre-commit hooks for code quality

### Code Quality Standards

- Python 3.9+ compatibility required
- Uses black for formatting, ruff for linting, mypy for type checking
- Strict mypy configuration with comprehensive type checking
- Extensive pre-commit hooks including spell checking and formatting
- 100% test coverage expected (`--cov=src/hebrew_numbers`)

## Testing

Tests are run with pytest and include:

- Doctests in modules (`--doctest-modules`)
- Coverage reporting
- Reverse execution order (`--reverse`)
- Strict markers and config

## Documentation

- Uses MkDocs for documentation
- `uv run just build-docs` - Build documentation
- `uv run just serve-docs` - Serve documentation locally
