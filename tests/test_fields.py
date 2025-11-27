from enum import Enum

import pytest
from pytest import MonkeyPatch

from envkit import Env

# str


def test_str_found(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_FOUND", "value")
    assert Env.str("TEST_FOUND") == "value"


def test_str_too_small(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_GOOD", "1")
    assert Env.str("TEST_GOOD", min_length=1) == "1"

    monkeypatch.setenv("TEST_TOO_SMALL", "")
    with pytest.raises(ValueError):
        Env.str("TEST_TOO_SMALL", min_length=1)


def test_str_too_large(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_GOOD", "1")
    assert Env.str("TEST_GOOD", max_length=1) == "1"

    monkeypatch.setenv("TEST_TOO_LARGE", "12")
    with pytest.raises(ValueError):
        Env.str("TEST_TOO_LARGE", max_length=1)


def test_str_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_DEFAULT_idk", raising=False)
    assert Env.str("TEST_DEFAULT_idk", required=False, default="idk") == "idk"
    monkeypatch.delenv("TEST_DEFAULT_None", raising=False)
    assert Env.str("TEST_DEFAULT_None", required=False, default=None) is None

    monkeypatch.setenv("TEST_DEFAULT_SET", "SET")
    assert Env.str("TEST_DEFAULT_SET", required=False, default="idk") == "SET"


def test_str_missing(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_MISSING", raising=False)
    with pytest.raises(KeyError):
        Env.str("TEST_MISSING")


# int


def test_int_found(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_FOUND", "1")
    assert Env.int("TEST_FOUND") == 1


def test_int_strip(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_FOUND", " 1 ")
    assert Env.int("TEST_FOUND") == 1


def test_int_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_INVALID", "a")
    with pytest.raises(ValueError):
        Env.int("TEST_INVALID")


def test_int_too_small(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_GOOD", "1")
    assert Env.int("TEST_GOOD", min_value=1) == 1

    monkeypatch.setenv("TEST_TOO_SMALL", "0")
    with pytest.raises(ValueError):
        Env.int("TEST_TOO_SMALL", min_value=1)


def test_int_too_large(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_GOOD", "1")
    assert Env.int("TEST_GOOD", max_value=1) == 1

    monkeypatch.setenv("TEST_TOO_LARGE", "2")
    with pytest.raises(ValueError):
        Env.int("TEST_TOO_LARGE", max_value=1)


def test_int_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_DEFAULT_idk", raising=False)
    assert Env.int("TEST_DEFAULT_1", required=False, default=1) == 1
    monkeypatch.delenv("TEST_DEFAULT_None", raising=False)
    assert Env.int("TEST_DEFAULT_None", required=False, default=None) is None

    monkeypatch.setenv("TEST_DEFAULT_SET", "1")
    assert Env.int("TEST_DEFAULT_SET", required=False, default=0) == 1


def test_int_missing(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_MISSING", raising=False)
    with pytest.raises(KeyError):
        Env.int("TEST_MISSING")


# bool


def test_bool_values(monkeypatch: MonkeyPatch) -> None:
    for key in ["true", "1", "yes", "on"]:
        monkeypatch.setenv(f"TEST_{key}", key)
        assert Env.bool(f"TEST_{key}") is True
    for key in ["false", "0", "no", "off"]:
        monkeypatch.setenv(f"TEST_{key}", key)
        assert Env.bool(f"TEST_{key}") is False


def test_bool_strip(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_TRUE", " true ")
    assert Env.bool("TEST_TRUE") is True


def test_bool_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_INVALID", "idk")
    with pytest.raises(ValueError):
        Env.bool("TEST_INVALID")


def test_bool_uppercase(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_TRUE", "TRUE")
    assert Env.bool("TEST_TRUE") is True


def test_bool_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_DEFAULT_True", raising=False)
    assert Env.bool("TEST_DEFAULT_True", required=False, default=True) is True
    monkeypatch.delenv("TEST_DEFAULT_None", raising=False)
    assert Env.bool("TEST_DEFAULT_None", required=False, default=None) is None

    monkeypatch.setenv("TEST_DEFAULT_SET", "false")
    assert Env.bool("TEST_DEFAULT_SET", required=False, default=True) is False


def test_bool_missing(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_MISSING", raising=False)
    with pytest.raises(KeyError):
        Env.bool("TEST_MISSING")


# enum


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def test_enum_found(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_FOUND", "RED")
    assert Env.enum("TEST_FOUND", Color) == Color.RED


def test_enum_strip(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_FOUND", " RED ")
    assert Env.enum("TEST_FOUND", Color) == Color.RED


def test_enum_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_INVALID", "bad")
    with pytest.raises(ValueError):
        Env.enum("TEST_INVALID", Color)


def test_enum_case_insensitive(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_BAD", "red")
    with pytest.raises(ValueError):
        Env.enum("TEST_BAD", Color, case_sensitive=True)
    monkeypatch.setenv("TEST_GOOD", "red")
    assert Env.enum("TEST_GOOD", Color, case_sensitive=False) == Color.RED


def test_enum_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_DEFAULT_RED", raising=False)
    assert (
        Env.enum("TEST_DEFAULT_RED", Color, required=False, default=Color.RED)
        == Color.RED
    )
    monkeypatch.delenv("TEST_DEFAULT_None", raising=False)
    assert Env.enum("TEST_DEFAULT_None", Color, required=False, default=None) is None

    monkeypatch.setenv("TEST_DEFAULT_SET", "RED")
    assert (
        Env.enum("TEST_DEFAULT_SET", Color, required=False, default=Color.BLUE)
        == Color.RED
    )


def test_enum_missing(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_MISSING", raising=False)
    with pytest.raises(KeyError):
        Env.enum("TEST_MISSING", Color)


# literal

CHOICES = ("1", "2")


def test_literal_found(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_FOUND", "1")
    assert Env.literal("TEST_FOUND", CHOICES) == "1"


def test_literal_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_INVALID", "a")
    with pytest.raises(ValueError):
        Env.literal("TEST_INVALID", CHOICES)


def test_literal_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_DEFAULT_1", raising=False)
    assert Env.literal("TEST_DEFAULT_1", CHOICES, required=False, default="1") == "1"
    monkeypatch.delenv("TEST_DEFAULT_None", raising=False)
    assert (
        Env.literal("TEST_DEFAULT_None", CHOICES, required=False, default=None) is None
    )

    monkeypatch.setenv("TEST_DEFAULT_SET", "1")
    assert Env.literal("TEST_DEFAULT_SET", CHOICES, required=False, default="0") == "1"


def test_literal_missing(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_MISSING", raising=False)
    with pytest.raises(KeyError):
        Env.literal("TEST_MISSING", CHOICES)
