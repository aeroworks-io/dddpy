from ulid import ULID


from ..common import BaseClass, PrimitiveBase


class ID(PrimitiveBase, ULID):
    coerce = True

    def __repr__(self):
        return f"{self.__class__.__name__}('{str(self)}')"

    def __json__(self):
        return str(self)

    @classmethod
    def validate(cls, v):
        if isinstance(v, cls):
            return v
        if cls.coerce:
            return cls.__restore__(v)
        raise TypeError(f"expected {repr(v)} to be a instance of {cls}")

    @classmethod
    def __generate__(cls):
        return cls()

    @classmethod
    def __restore__(cls, value):
        return cls.from_str(str(value))


class Entity(BaseClass):
    id: ID

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id


class Value(BaseClass):
    class Config:
        allow_mutation = False
