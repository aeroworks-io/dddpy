from typing import Any, Optional

from pydantic import BaseModel, BaseConfig, ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import FieldInfo as _FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable
from pydantic.utils import ROOT_KEY

from .abstract import JsonSerializable, Restoreable, Generatable
from .primitive import PrimitiveBase, Primitive


class BaseClass(Restoreable, Generatable, JsonSerializable, BaseModel):
    class Config(BaseConfig):
        json_encoders = {JsonSerializable: lambda ins: ins.__json__()}

    def __init__(self, *args, **kwargs):
        kw = tuple(self.__class__.__annotations__)
        if len(args) > len(kw):
            raise TypeError(
                f"{self.__class__.__name__}.__init__() takes {len(kw)} positional argument but {len(args)} were "
                f"given"
            )
        super().__init__(**dict(zip(kw, args)), **kwargs)

    @classmethod
    def parse_obj(cls, obj: Any):
        obj = cls._enforce_dict_if_root(obj)
        if not isinstance(obj, dict):
            try:
                obj = dict(obj)
            except (TypeError, ValueError) as e:
                exc = TypeError(
                    f"{cls.__name__} expected dict not {obj.__class__.__name__}"
                )
                raise ValidationError([ErrorWrapper(exc, loc=ROOT_KEY)], cls) from e
        return super().parse_obj(
            {
                k: typ.__restore__(v)
                if issubclass((typ := cls.__annotations__[k]), Restoreable)
                else v
                for k, v in obj.items()
            }
        )

    def __json__(self) -> str:
        return self.json()

    @classmethod
    def __restore__(cls, value: Any):
        return cls.parse_obj(value)

    @classmethod
    def __generate__(cls):
        # noinspection PyArgumentList
        return cls(
            **{
                key: typ.__generate__()
                for key, typ in cls.__annotations__.items()
                if issubclass(typ, Generatable)
            }
        )


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
        raise ValueError("cannot specify both default and default_factory")

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
