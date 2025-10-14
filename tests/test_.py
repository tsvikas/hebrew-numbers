import importlib.metadata

import hebrew_numbers


def test_version() -> None:
    assert importlib.metadata.version("hebrew_numbers") == hebrew_numbers.__version__
