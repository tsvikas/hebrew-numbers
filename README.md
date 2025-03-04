# hebrew-numbers

[![Tests][tests-badge]][tests-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![uv][uv-badge]][uv-link]
[![Ruff][ruff-badge]][ruff-link]
[![Black][black-badge]][black-link]
\
[![PyPI version][pypi-version-badge]][pypi-link]
[![PyPI platforms][pypi-platforms-badge]][pypi-link]
[![Total downloads][pepy-badge]][pepy-link]
\
[![Made Using tsvikas/python-template][template-badge]][template-link]
[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![PRs Welcome][prs-welcome-badge]][prs-welcome-link]

## Overview

This library provides a comprehensive solution for working with Hebrew numbers in various contexts.
Hebrew has unique and complex rules for number representation that vary based on gender, definiteness, and usage context.
This library aims to simplify these complexities by providing intuitive functions for converting numerical values to their proper Hebrew textual representation.

## Usage

Install the package using pip, or with a dependency manager like uv:

```bash
pip install hebrew-numbers
```

and import the package in your code:

```python
import hebrew_numbers
```

### Indefinite Number -- מספר סתמי

When counting without specific nouns, but rather in a general sense, we use the indefinite number.

```pycon
>>> [indefinite_number(n) for n in [1, 2, 3]]
['אחת', 'שתיים', 'שָלוש']
>>> indefinite_number(0)
'אפס'
>>> indefinite_number(-3)
'מינוס שָלוש'
>>> indefinite_number(1234567890)
'מיליארד מאתיים שלושים וארבעה מיליון חמש מאות שישים ושבעה אלף שמונֶה מאות ותשעים'
```

### Ordinal Number -- מספר סודר

A number that describes the position of an object in a series is called an ordinal number.
This number can be masculine (זכר) or feminine (נקבה).

```pycon
>>> [ordinal_number(n, "M") for n in [1, 2, 3]]
['ראשון', 'שני', 'שלישי']
>>> [ordinal_number(n, "F") for n in [1, 2, 3]]
['ראשונה', 'שנייה', 'שלישית']
```

### Cardinal Number -- מספר מונה

#### Usage with noun

Cardinal numbers are used to indicate quantities. Their form depends on the following factors:

- The gender of the noun (masculine or feminine).
- Whether the noun is definite (מיודע) or indefinite (סתמי).

To specify a quantity with a noun, use `count_noun(n, singular_form, plural_form, gender, definite)`.

| Number | Masculine, Indefinite                                | Masculine, Definite                                   | Feminine, Indefinite                                  | Feminine, Definite                                     |
| ------ | ---------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| `n`    | `count_noun(n, "ילד", "ילדים", "M", definite=False)` | `count_noun(n, "הילד", "הילדים", "M", definite=True)` | `count_noun(n, "ילדה", "ילדות", "F", definite=False)` | `count_noun(n, "הילדה", "הילדות", "F", definite=True)` |
| 1      | ילד אֶחָד                                              | הילד האֶחָד                                             | ילדה אחת                                              | הילדה האחת                                             |
| 2      | שני ילדים                                            | שני הילדים                                            | שתי ילדות                                             | שתי הילדות                                             |
| 3      | שלושה ילדים                                          | שלושת הילדים                                          | שָלוש ילדות                                            | שְלוש הילדות                                            |

If you only need the numerical prefix, use `count_prefix(n, gender, definite)`.

#### Absolute and Construct Forms

The number itself can be masculine (זכר) or feminine (נקבה), and absolute (נפרד) or construct (נסמך).
If you know the gender and construct state, you can the number itself with `cardinal_number(n, gender, construct)`

| Number | Masculine, Absolute                        | Masculine, Construct                      | Feminine, Absolute                         | Feminine, Construct                       |
| ------ | ------------------------------------------ | ----------------------------------------- | ------------------------------------------ | ----------------------------------------- |
| `n`    | `cardinal_number(n, "M", construct=False)` | `cardinal_number(n, "M", construct=True)` | `cardinal_number(n, "F", construct=False)` | `cardinal_number(n, "F", construct=True)` |
| 1      | אֶחָד                                        | אַחַד                                       | אחת                                        | אחת                                       |
| 2      | שניים                                      | שני                                       | שתיים                                      | שתי                                       |
| 3      | שלושה                                      | שלושת                                     | שָלוש                                       | שְלוש                                      |

##### Notes

- The indefinite number is the feminine-absolute form.
- The form of the number following "פי" (times/multiplied by) to be in the masculine-absolute form: פי שניים, פי שלושה, פי ארבעה.
- Use the masculine-absolute form to indicate the days of the month: אחד בכסלו, עשרה בטבת, אחד באפריל, שניים ביוני.

## Development

- install [git][install-git], [uv][install-uv].
- git clone this repo: `git clone tsvikas/hebrew-numbers.git`
- run `uv run just prepare`

### Code quality

- use `uv run just format` to format the code.
- use `uv run just lint` to see linting errors.
- use `uv run just test` to see run tests.
- use `uv run just check` to run all the checks (format, lint, test, and pre-commit).
- Run a specific tool directly, with `uv run pytest`/`ruff`/`mypy`/`black`/...

### Build

- run formatting, linting, and tests.
- use
  `VER="vX.Y.Z" && git tag -a "$VER" -m "version $VER" -e && git push origin tag "$VER"`
- use `uv build` to build

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]: https://github.com/psf/black
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]: https://github.com/tsvikas/hebrew-numbers/discussions
[install-git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[install-uv]: https://docs.astral.sh/uv/getting-started/installation/
[pepy-badge]: https://img.shields.io/pepy/dt/hebrew-numbers
[pepy-link]: https://pepy.tech/project/hebrew-numbers
[prs-welcome-badge]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
[prs-welcome-link]: http://makeapullrequest.com
[pypi-link]: https://pypi.org/project/hebrew-numbers/
[pypi-platforms-badge]: https://img.shields.io/pypi/pyversions/hebrew-numbers
[pypi-version-badge]: https://img.shields.io/pypi/v/hebrew-numbers
[rtd-badge]: https://readthedocs.org/projects/hebrew-numbers/badge/?version=latest
[rtd-link]: https://hebrew-numbers.readthedocs.io/en/latest/?badge=latest
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff-link]: https://github.com/astral-sh/ruff
[template-badge]: https://img.shields.io/badge/%F0%9F%9A%80_Made_Using-tsvikas%2Fpython--template-gold
[template-link]: https://github.com/tsvikas/python-template
[tests-badge]: https://github.com/tsvikas/hebrew-numbers/actions/workflows/ci.yml/badge.svg
[tests-link]: https://github.com/tsvikas/hebrew-numbers/actions/workflows/ci.yml
[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
[uv-link]: https://github.com/astral-sh/uv
