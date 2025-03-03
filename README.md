# hebrew-numbers

[![Tests][tests-badge]][tests-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![uv][uv-badge]][uv-link]
[![Ruff][ruff-badge]][ruff-link]
[![Black][black-badge]][black-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![PRs Welcome][prs-welcome-badge]][prs-welcome-link]
[![Total downloads][pepy-badge]][pepy-link]

Made using [tsvikas/python-template](http://github.com/tsvikas/python-template)

## Usage

### Cardinal Number -- מספר מונה

```pycon
>>> cardinal_number(1234, "F", construct=False)
'אלף מאתיים שלושים וארבע'
>>> cardinal_number(1234, "M", construct=False)
'אלף מאתיים שלושים וארבעה'
>>> cardinal_number(3, "F", construct=True)
'שְלוש'
>>> cardinal_number(3, "M", construct=True)
'שלושת'
```

### Indefinite Number -- מספר סתמי

```pycon
>>> indefinite_number(-3)
'מינוס שָלוש'
>>> indefinite_number(1234567)
'מיליון מאתיים שלושים וארבעה אלף חמש מאות שישים ושבע'
```

### Ordinal Number -- מספר סודר

```pycon
>>> ordinal_number(1, "M")
'ראשון'
>>> ordinal_number(2, "F")
'שנייה'
```

### מספר מונה ושם עצם

```pycon
>>> count_noun(1, "ילד", "ילדים", "M", definite=False)
'ילד אֶחָד'
>>> count_noun(1, "הילדה", "הילדות", "F", definite=True)
'הילדה האחת'
>>> count_prefix(3, "M", definite=False)
'שלושה'
>>> count_noun(3, "ילד", "ילדים", "M", definite=False)
'שלושה ילדים'
>>> count_prefix(3, "F", definite=False)
'שָלוש'
>>> count_noun(3, "ילדה", "ילדות", "F", definite=False)
'שָלוש ילדות'
>>> count_prefix(3, "M", definite=True)
'שלושת'
>>> count_noun(3, "הילד", "הילדים", "M", definite=True)
'שלושת הילדים'
>>> count_prefix(3, "F", definite=True)
'שְלוש'
>>> count_noun(3, "הילדה", "הילדות", "F", definite=True)
'שְלוש הילדות'
```

## Development

- install [git][install-git], [uv][install-uv].
- git clone this repo
- run `uv run just prepare`

## Code formatting

- use `uv run black .` to format code
- use
  `git ls-files -z -- '*.md' '*.rst' '*.tex' '*.py' | xargs -0 uv run blacken-docs`
  to format docs

## Code quality

- use `uv run ruff check .` to verify code quality
- use `uv run mypy` to verify check typing
- use `uv run pytest` to run tests

## Build

- run formatting, linting, and tests.
- optionally, use `uv run dunamai from git` to see the current version
- use
  `VER="vX.Y.Z" && git tag -a "$VER" -m "version $VER" -e && git push origin tag "$VER"`
- use `uv build` to build

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]: https://github.com/psf/black
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/hebrew-numbers
[conda-link]: https://github.com/conda-forge/hebrew-numbers-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]: https://github.com/tsvikas/hebrew-numbers/discussions
[install-git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[install-uv]: https://docs.astral.sh/uv/getting-started/installation/
[pepy-badge]: https://static.pepy.tech/badge/hebrew-numbers
[pepy-link]: https://pepy.tech/project/hebrew-numbers
[prs-welcome-badge]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
[prs-welcome-link]: http://makeapullrequest.com
[pypi-link]: https://pypi.org/project/hebrew-numbers/
[pypi-platforms]: https://img.shields.io/pypi/pyversions/hebrew-numbers
[pypi-version]: https://img.shields.io/pypi/v/hebrew-numbers
[rtd-badge]: https://readthedocs.org/projects/hebrew-numbers/badge/?version=latest
[rtd-link]: https://hebrew-numbers.readthedocs.io/en/latest/?badge=latest
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff-link]: https://github.com/astral-sh/ruff
[tests-badge]: https://github.com/tsvikas/hebrew-numbers/actions/workflows/ci.yml/badge.svg
[tests-link]: https://github.com/tsvikas/hebrew-numbers/actions/workflows/ci.yml
[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
[uv-link]: https://github.com/astral-sh/uv
