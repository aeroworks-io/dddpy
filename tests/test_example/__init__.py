from unittest import TestCase

import pytest
from pydantic import UUID4, ValidationError

from example import User, UserID, UserName


class TestExample(TestCase):
    def test_user_creation(self):
        user = User(
            id=UserID(raw=UUID4("00000000-0000-4000-8000-000000000000")),
            name=UserName(value="John Doe")
        )
        assert user
        assert user.id == UserID(raw=UUID4("00000000-0000-4000-8000-000000000000"))
        assert user.name == UserName(value="John Doe")

    def test_validation_error(self):
        with pytest.raises(ValidationError):
            User(
                id=UserID(raw=UUID4("00000000-0000-4000-0000-000000000000")),
                name=UserName(value="John Doe")
            )
