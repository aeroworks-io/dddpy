from unittest.case import TestCase

import pytest

from dddpy import ID, Entity, Field


class IDTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class StrictID(ID):
            coerce = False

        self.cls = StrictID

    def test_valid_id(self):
        assert isinstance(self.cls.__generate__(), ID)

    def test_json(self):
        assert self.cls.__generate__().__json__()

    def test_repr(self):
        assert repr(self.cls.__generate__())

    def test_validator_error(self):
        with pytest.raises(TypeError):
            self.cls.validate(str(self.cls()))


class TestEntity(TestCase):
    def test_entity_basic_generation(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        assert User(id=UserID(), name="John Doe")

    def test_entity_comparison(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        user = User(id=UserID(), name="John Doe")
        assert user == user

    def test_entity_comparison_false(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        user = User(id=UserID(), name="John Doe")
        user2 = User(id=UserID(), name="Jane Doe")
        assert user != user2

    def test_entity_comparison_different(self):
        class UserID(ID):
            ...

        class User(Entity):
            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        user = User(id=UserID(), name="John Doe")
        user2 = user.dict()
        assert user != user2

    def test_invalid_field(self):
        class UserID(ID):
            ...

        with pytest.raises(ValueError):

            class User(Entity):
                id: UserID = Field(..., description="User's id")
                name: str = Field(
                    "John Doe", description="Users's name", default_factory=str
                )
