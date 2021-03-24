from abc import ABC, abstractmethod
from typing import TypeVar, Type, Any, Optional

from pydantic.fields import ModelField

T = TypeVar("T")
GenericAlias = type(Optional[int])


class Restoreable(ABC):
    @classmethod
    @abstractmethod
    def __restore__(cls: Type[T], value) -> T:
        ...


class Generatable(ABC):
    @classmethod
    @abstractmethod
    def __generate__(cls: Type[T]) -> T:
        ...


class JsonSerializable(ABC):
    @abstractmethod
    def __json__(self: T) -> Any:
        ...


def find_abstract_constraint(annotation, abstract: Type[T]) -> Optional[T]:
    if type(annotation) is GenericAlias:
        for ann in annotation.__args__:
            constraint = find_abstract_constraint(ann, abstract)
            if constraint:
                return constraint
    try:
        if issubclass(annotation, abstract):
            return annotation
    except TypeError:
        return None


def restore(fields, key, value):
    field: ModelField = fields.get(key)
    if not field:
        for _field in fields.values():
            if _field.alias == key:
                field = _field
                break
        else:
            return value
    annotation = field.type_
    if value is None and field.allow_none:
        return value
    if typ := find_abstract_constraint(annotation, Restoreable):
        return typ.__restore__(value)
    return value
