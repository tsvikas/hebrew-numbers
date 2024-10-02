hebrew_numerals
==========
## Usage

## Development
* install git, python3.12, poetry, poethepoet.
* git clone this repo
* create a venv using `poetry env use python3.12; poetry install`
* enable pre-commit checks with `poetry run pre-commit install`
* use `poe check` to verify code quality

## Build
* install poetry-dynamic-versioning[plugin]
* use `poe version` to see the current version
* use `poe tag vX.Y.Z` to add a git tag. you still need to push it.
* use `poetry build` to build
