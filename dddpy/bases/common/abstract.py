from abc import ABC, abstractmethod
from typing import TypeVar, Type, Any, Optional

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
