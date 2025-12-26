# pyright: reportUnusedCallResult=false

from enum import Enum, auto

import pytest
from pytest import MonkeyPatch

from envkit import Env

ENV_KEY = "ENV_KEY"


class TestStr:
    def test_found(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        assert Env.str(ENV_KEY) == "a"

    def test_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        with pytest.raises(KeyError):
            Env.str(ENV_KEY)

    def test_default_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.str(ENV_KEY, required=False, default="a") == "a"

    def test_default_none_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.str(ENV_KEY, required=False, default=None) is None

    def test_default_ignored_when_present(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        assert Env.str(ENV_KEY, required=False, default="b") == "a"

    def test_strip_disabled(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " a ")
        assert Env.str(ENV_KEY, strip=False) == " a "

    def test_strip_enabled(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " a ")
        assert Env.str(ENV_KEY, strip=True) == "a"

    def test_min_length_enforced_after_strip(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " a ")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, strip=True, min_length=2)

    def test_min_length_at_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        assert Env.str(ENV_KEY, min_length=1) == "a"

    def test_min_length_below_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, min_length=1)

    def test_max_length_at_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        assert Env.str(ENV_KEY, max_length=1) == "a"

    def test_max_length_above_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "ab")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, max_length=1)

    def test_invalid_range(self) -> None:
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, min_length=2, max_length=1)

    def test_allow_empty_enabled(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "")
        assert Env.str(ENV_KEY, allow_empty=True) == ""

    def test_allow_empty_disabled(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, allow_empty=False)

    def test_allow_empty_when_space_not_stripped(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        monkeypatch.setenv(ENV_KEY, " ")
        assert Env.str(ENV_KEY, allow_empty=False, strip=False) == " "

    def test_allow_empty_when_stripped_space(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " ")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, allow_empty=False, strip=True)

    def test_allow_empty_invalid_with_min_length_zero(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, allow_empty=False, min_length=0)

    def test_allow_empty_invalid_with_max_length_zero(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.str(ENV_KEY, allow_empty=False, max_length=0)


class TestInt:
    def test_found(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1")
        assert Env.int(ENV_KEY) == 1

    def test_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        with pytest.raises(KeyError):
            Env.int(ENV_KEY)

    def test_default_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.int(ENV_KEY, required=False, default=1) == 1

    def test_default_none_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.int(ENV_KEY, required=False, default=None) is None

    def test_default_ignored_when_present(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1")
        assert Env.int(ENV_KEY, required=False, default=0) == 1

    def test_invalid(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.int(ENV_KEY)

    def test_strip_whitespace(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " 1 ")
        assert Env.int(ENV_KEY) == 1

    def test_min_value_at_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1")
        assert Env.int(ENV_KEY, min_value=1) == 1

    def test_min_value_below_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "0")
        with pytest.raises(ValueError):
            Env.int(ENV_KEY, min_value=1)

    def test_max_value_at_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1")
        assert Env.int(ENV_KEY, max_value=1) == 1

    def test_max_value_above_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "2")
        with pytest.raises(ValueError):
            Env.int(ENV_KEY, max_value=1)

    def test_invalid_range(self) -> None:
        with pytest.raises(ValueError):
            Env.int(ENV_KEY, min_value=2, max_value=1)


class TestFloat:
    def test_found(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1.2")
        assert Env.float(ENV_KEY) == 1.2

    def test_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        with pytest.raises(KeyError):
            Env.float(ENV_KEY)

    def test_default_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.float(ENV_KEY, required=False, default=1.2) == 1.2

    def test_default_none_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.float(ENV_KEY, required=False, default=None) is None

    def test_default_ignored_when_present(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1.2")
        assert Env.float(ENV_KEY, required=False, default=1.1) == 1.2

    def test_invalid(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.float(ENV_KEY)

    @pytest.mark.parametrize("invalid_value", ["nan", "inf", "-inf"])
    def test_non_finite_invalid(
        self, monkeypatch: MonkeyPatch, invalid_value: str
    ) -> None:
        monkeypatch.setenv(ENV_KEY, invalid_value)
        with pytest.raises(ValueError):
            Env.float(ENV_KEY)

    def test_strip_whitespace(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " 1.2 ")
        assert Env.float(ENV_KEY) == 1.2

    def test_min_value_at_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1.2")
        assert Env.float(ENV_KEY, min_value=1.2) == 1.2

    def test_min_value_below_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1.2")
        with pytest.raises(ValueError):
            Env.float(ENV_KEY, min_value=1.3)

    def test_max_value_at_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1.2")
        assert Env.float(ENV_KEY, max_value=1.2) == 1.2

    def test_max_value_above_boundary(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1.2")
        with pytest.raises(ValueError):
            Env.float(ENV_KEY, max_value=1.1)

    def test_invalid_range(self) -> None:
        with pytest.raises(ValueError):
            Env.float(ENV_KEY, min_value=1.2, max_value=1.1)


class TestBool:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("true", True),
            ("1", True),
            ("yes", True),
            ("on", True),
            ("false", False),
            ("0", False),
            ("no", False),
            ("off", False),
        ],
    )
    def test_values(self, monkeypatch: MonkeyPatch, value: str, expected: bool) -> None:
        monkeypatch.setenv(ENV_KEY, value)
        assert Env.bool(ENV_KEY) is expected

    def test_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        with pytest.raises(KeyError):
            Env.bool(ENV_KEY)

    def test_default_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.bool(ENV_KEY, required=False, default=True) is True

    def test_default_none_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.bool(ENV_KEY, required=False, default=None) is None

    def test_default_ignored_when_present(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "false")
        assert Env.bool(ENV_KEY, required=False, default=True) is False

    def test_invalid(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.bool(ENV_KEY)

    def test_strip_whitespace(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " true ")
        assert Env.bool(ENV_KEY) is True

    def test_uppercase(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "TRUE")
        assert Env.bool(ENV_KEY) is True


class ValidEnum(Enum):
    RED = auto()
    BLUE = auto()


class CaseInsensitiveConflictEnum(Enum):
    RED = auto()
    red = auto()


class TestEnum:
    def test_found(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, ValidEnum.RED.name)
        assert Env.enum(ENV_KEY, ValidEnum) == ValidEnum.RED

    def test_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        with pytest.raises(KeyError):
            Env.enum(ENV_KEY, ValidEnum)

    def test_default_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert (
            Env.enum(ENV_KEY, ValidEnum, required=False, default=ValidEnum.RED)
            == ValidEnum.RED
        )

    def test_default_none_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.enum(ENV_KEY, ValidEnum, required=False, default=None) is None

    def test_default_ignored_when_present(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, ValidEnum.RED.name)
        assert (
            Env.enum(ENV_KEY, ValidEnum, required=False, default=ValidEnum.BLUE)
            == ValidEnum.RED
        )

    def test_invalid(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.enum(ENV_KEY, ValidEnum)

    def test_strip_whitespace(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, f" {ValidEnum.RED.name} ")
        assert Env.enum(ENV_KEY, ValidEnum) == ValidEnum.RED

    def test_case_insensitive_lowercase(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, ValidEnum.RED.name.lower())
        assert Env.enum(ENV_KEY, ValidEnum, case_sensitive=False) == ValidEnum.RED

    def test_case_sensitive_lowercase(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, ValidEnum.RED.name.lower())
        with pytest.raises(ValueError):
            Env.enum(ENV_KEY, ValidEnum, case_sensitive=True)

    def test_case_insensitive_invalid(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.enum(ENV_KEY, ValidEnum, case_sensitive=False)

    def test_case_insensitive_conflict(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, ValidEnum.RED.name)
        with pytest.raises(ValueError):
            Env.enum(ENV_KEY, CaseInsensitiveConflictEnum, case_sensitive=False)


CHOICES = ("1", "2")


class TestLiteral:
    def test_found(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1")
        assert Env.literal(ENV_KEY, CHOICES) == "1"

    def test_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        with pytest.raises(KeyError):
            Env.literal(ENV_KEY, CHOICES)

    def test_default_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.literal(ENV_KEY, CHOICES, required=False, default="1") == "1"

    def test_default_none_when_missing(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.delenv(ENV_KEY, raising=False)
        assert Env.literal(ENV_KEY, CHOICES, required=False, default=None) is None

    def test_default_ignored_when_present(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "1")
        assert Env.literal(ENV_KEY, CHOICES, required=False, default="2") == "1"

    def test_invalid(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.literal(ENV_KEY, CHOICES)

    def test_strip_disabled(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " 1 ")
        with pytest.raises(ValueError):
            Env.literal(ENV_KEY, CHOICES, strip=False)

    def test_strip_enabled(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, " 1 ")
        assert Env.literal(ENV_KEY, CHOICES, strip=True) == "1"

    def test_empty_choices(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv(ENV_KEY, "a")
        with pytest.raises(ValueError):
            Env.literal(ENV_KEY, choices=())

    def test_default_not_in_choices(self) -> None:
        with pytest.raises(ValueError):
            Env.literal(ENV_KEY, choices=(), required=False, default="a")
