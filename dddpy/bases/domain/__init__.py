import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, UUID4
from pydantic.fields import FieldInfo as _FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable


class IDBase(ABC):
    raw: Any

    @classmethod
    @abstractmethod
    def generate(cls):
        ...


class ID(BaseModel, IDBase):
    raw: UUID4

    @classmethod
    def generate(cls):
        return cls(raw=UUID4(str(uuid.uuid4())))


class Entity(BaseModel):
    id: ID

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id


class Value(BaseModel):
    ...


class FieldInfo(_FieldInfo):
    ...


# noinspection PyPep8Naming
def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: str = None,
    title: str = None,
    description: str = None,
    const: bool = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    min_items: int = None,
    max_items: int = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    **extra: Any,
) -> Any:
    if default is not Undefined and default_factory is not None:
        raise ValueError('cannot specify both default and default_factory')

    return FieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        min_items=min_items,
        max_items=max_items,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        **extra,
    )
