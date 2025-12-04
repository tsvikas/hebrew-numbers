# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.2.1] - 2025-12-05

### Added

- Type stub (`_version.pyi`) for `__version__`

## [0.2.0] - 2025-01-16

### Added

- Jinja2 extension for Hebrew number conversion with bilingual filter support
- English-named filters: `hebrew_indefinite`, `hebrew_cardinal`, `hebrew_ordinal`, `hebrew_count`, `hebrew_prefix`
- Hebrew-named filters: `מספר_סתמי`, `מספר_מונה`, `מספר_סודר`, `כמות_של`, `כמות` - enabling fully Hebrew template syntax for improved readability
- Support for Hebrew parameter values (`'כן'`/`'לא'` for booleans, `'ז'`/`'נ'` for gender, `'נפרד'`/`'נסמך'` for construct state)
- Optional jinja2 installation via `hebrew-numbers[jinja]` extra

## [0.1.1] - 2025-01-16

### Changed

- Updated copyright notice format
- Improved docstring formatting and examples
- Enhanced function documentation with detailed Args, Returns, and Raises sections
- Code quality improvements and linting fixes

## [0.1.0] - 2025-01-16

### Added

- Initial release of Hebrew numbers conversion library
- Core functions for Hebrew number conversion:
  - `indefinite_number()` - General counting without specific nouns
  - `ordinal_number()` - Position in series (1st, 2nd, etc.)
  - `cardinal_number()` - Basic number with gender and construct state
  - `count_noun()` - Full noun counting with proper grammar
  - `count_prefix()` - Just the numerical prefix
- Support for Hebrew grammatical gender (masculine/feminine)
- Support for construct state and definiteness
- Comprehensive test coverage
- Documentation and examples
- CI/CD pipeline with GitHub Actions

[0.1.0]: https://github.com/tsvikas/hebrew-numbers/releases/tag/v0.1.0
[0.1.1]: https://github.com/tsvikas/hebrew-numbers/compare/v0.1.0...v0.1.1
[0.2.0]: https://github.com/tsvikas/hebrew-numbers/compare/v0.1.1...v0.2.0
[0.2.1]: https://github.com/tsvikas/hebrew-numbers/compare/v0.2.0...v0.2.1
[unreleased]: https://github.com/tsvikas/hebrew-numbers/compare/v0.2.1...HEAD
