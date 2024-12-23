hebrew_numbers
==========
## Usage
### מספר מונה
```
>>> cardinal_number(1234, "F", construct=False)
'אלף מאתיים שלושים וארבע'
>>> cardinal_number(1234, "M", construct=False)
'אלף מאתיים שלושים וארבעה'
>>> cardinal_number(3, "F", construct=True)
'שְלוש'
>>> cardinal_number(3, "M", construct=True)
'שלושת'
```

### מספר סתמי
```
>>> indefinite_number(-3)
'מינוס שָלוש'
>>> indefinite_number(1234567)
'מיליון מאתיים שלושים וארבעה אלף חמש מאות שישים ושבע'
```

### מספר סודר
```
>>> ordinal_number(1, "M")
'ראשון'
>>> ordinal_number(2, "F")
'שנייה'
```

### מספר מונה ושם עצם
```
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
