from abc import ABC, abstractmethod

from .abstract import JsonSerializable, Restoreable, Generatable


class PrimitiveBase(JsonSerializable, Restoreable, Generatable, ABC):
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
