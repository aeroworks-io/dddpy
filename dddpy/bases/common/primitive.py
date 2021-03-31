import re
from abc import ABC, abstractmethod
from typing import Dict, Any

from pydantic import ConstrainedStr
from ulid import ULID as _ULID, base32

from .abstract import JsonSerializable, Restoreable, Generatable, T


class PrimitiveBase(JsonSerializable, Restoreable, Generatable, ABC):
    @classmethod
    @abstractmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        ...

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    @abstractmethod
    def validate(cls, v):
        ...


class Primitive(PrimitiveBase):
    coerce = True

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        # using string as the default type as it's the natural type when encoding to JSON
        field_schema.update(type="string")

    @classmethod
    def validate(cls, v):
        if isinstance(v, cls):
            return v
        if cls.coerce:
            # noinspection PyArgumentList
            return cls(v)
        raise TypeError(f"expected {repr(v)} to be a instance of {cls}")

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __json__(self):
        return self

    @classmethod
    def __restore__(cls, value):
        # noinspection PyArgumentList
        return cls(value)

    @classmethod
    def __generate__(cls):
        return cls()


class ULID(_ULID, ConstrainedStr, PrimitiveBase):
    strip_whitespace = True
    min_length = 26
    max_length = 26
    regex = re.compile(
        r"^[0123456789abcdefghjkmnpqrstvwxyzABCDEFGHJKMNPQRSTVWXYZ]{26}$"
    )

    def __new__(cls, *args, **kwargs):
        if not args:
            args = (_ULID(),)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(ULID, self).__init__(base32.decode(self), *args[1:], **kwargs)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        # using string as the default type as it's the natural type when encoding to JSON
        super().__modify_schema__(field_schema)
        field_schema["format"] = "ulid"

    @classmethod
    def validate(cls, value):
        return cls(super().validate(value))

    @classmethod
    def from_bytes(cls, bytes_):
        return cls(_ULID.from_bytes(bytes_))

    @classmethod
    def from_str(cls, string):
        return cls(string)

    def __json__(self):
        return self

    @classmethod
    def __restore__(cls, value):
        return cls(value)

    @classmethod
    def __generate__(cls):
        return cls()
