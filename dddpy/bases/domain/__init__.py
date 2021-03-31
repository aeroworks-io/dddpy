from ..common import BaseClass
from ..common.primitive import ULID


class ID(ULID):
    def __repr__(self):
        return f"{self.__class__.__name__}('{str(self)}')"


class Entity(BaseClass):
    id: ID

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id


class Value(BaseClass):
    class Config:
        allow_mutation = False
