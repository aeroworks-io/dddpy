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
    def __init__(self, *args):
        super().__init__(*args)

        class UserID(ID):
            ...

        class User(Entity):
            """Class that represents a User"""

            id: UserID = Field(..., description="User's id")
            name: str = Field(..., description="Users's name")

        self.cls = User
        self.id_cls = UserID

    def test_entity_basic_generation(self):
        assert self.cls(id=self.id_cls(), name="John Doe")

    def test_entity_comparison(self):
        user = self.cls(id=self.id_cls(), name="John Doe")
        assert user == user

    def test_entity_comparison_false(self):
        user = self.cls(id=self.id_cls(), name="John Doe")
        user2 = self.cls(id=self.id_cls(), name="Jane Doe")
        assert user != user2

    def test_entity_comparison_different(self):
        user = self.cls(id=self.id_cls(), name="John Doe")
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

    def test_schema(self):
        assert self.cls.schema() == {
            "title": "User",
            "description": "Class that represents a User",
            "type": "object",
            "properties": {
                "id": {
                    "title": "Id",
                    "description": "User's id",
                    "type": "string",
                    "format": "ulid",
                    "pattern": "^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}$",
                },
                "name": {
                    "title": "Name",
                    "description": "Users's name",
                    "type": "string",
                },
            },
            "required": ["id", "name"],
        }
