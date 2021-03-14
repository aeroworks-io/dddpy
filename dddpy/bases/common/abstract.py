from abc import ABC, abstractmethod
from typing import TypeVar, Type, Any

T = TypeVar("T")


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
