from unittest import TestCase

import pytest

from dddpy import Value
from dddpy.bases.common.primitive import Primitive, ULID


class TestPrimitive(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Name(Primitive, str):
            """x coordinate"""

            coerce = False

            @classmethod
            def __generate__(cls):
                return cls("John Doe")

        self.cls = Name

    def test_valid(self):
        assert self.cls("John Doe")

    def test_schema(self):
        class A(Value):
            name: self.cls  # noqa

        assert A.schema() == {
            "properties": {"name": {"title": "Name", "type": "string"}},
            "required": ["name"],
            "title": "A",
            "type": "object",
        }

    def test_validator_invalid(self):
        with pytest.raises(TypeError):
            self.cls.validate("John Doe")

    def test_generate(self):
        assert self.cls.__generate__() == self.cls("John Doe")

    def test_repr(self):
        assert repr(self.cls.__generate__()) == "Name('John Doe')"

    def test_json(self):
        assert self.cls.__generate__().__json__() == "John Doe"


class TestULID(TestCase):
    @staticmethod
    def test_hash():
        assert hash(ULID())
