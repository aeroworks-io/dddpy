from unittest import TestCase

import pytest
from pydantic import ValidationError

from example import User, UserID, UserName


class TestExample(TestCase):
    def test_user_creation(self):
        user = User(
            id=UserID.from_str("00000000000000000000000000"), name=UserName("John Doe")
        )
        assert user
        assert user.id == UserID.from_str("00000000000000000000000000")
        assert user.name == UserName("John Doe")

    def test_user_generate(self):
        user = User.__generate__()
        assert user
        assert str(user.id)
        assert str(user.name)

    def test_validation_error(self):
        with pytest.raises(ValidationError):
            # noinspection PyTypeChecker
            User(
                id="00000000-0000-4000-0000-000000000000",
                name=UserName("John Doe"),
            )
