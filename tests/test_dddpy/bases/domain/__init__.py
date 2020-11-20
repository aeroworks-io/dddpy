from unittest.case import TestCase

import pytest

from dddpy import ID, IDBase, UUID4, Entity, Field


class IDTest(TestCase):
    def test_valid_id_base(self):
        class ValidID(IDBase):
            raw: int

            def __init__(self, raw: int):
                self.raw = raw

            @classmethod
            def generate(cls):
                return cls(raw=0)

        assert issubclass(ValidID, IDBase)
        assert ValidID.generate().raw == 0

    def test_invalid_id_base(self):
        class InvalidID(IDBase):
            raw: int

        with pytest.raises(TypeError):
            InvalidID()

    def test_valid_id(self):
        assert isinstance(ID.generate().raw, UUID4)


class TestEntity(TestCase):
    def test_entity_basic_generation(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        assert User(id=UserID.generate(), name="John Doe")

    def test_entity_comparison(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        user = User(id=UserID.generate(), name="John Doe")
        assert user == user

    def test_entity_comparison_false(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        user = User(id=UserID.generate(), name="John Doe")
        assert user != "user"

    def test_invalid_field(self):
        class UserID(ID):
            ...

        with pytest.raises(ValueError):
            class User(Entity):
                id: UserID = Field(..., description="User's id")
                name: str = Field("John Doe", description="Users's name", default_factory=str)
