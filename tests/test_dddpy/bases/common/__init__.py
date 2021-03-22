import json
from typing import Optional
from unittest import TestCase

import pytest
from pydantic import ValidationError

from dddpy import Primitive
from dddpy.bases.common import BaseClass


class TestBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class X(Primitive, int):
            """x coordinate"""

        class Y(Primitive, int):
            """y coordinate"""

        class A(BaseClass):
            x: X
            y: Optional[Y]
            z: Optional[int]

        self.cls = A

    def test_simple_class_valid(self):
        assert self.cls(x=1, y=2)

    def test_simple_class_args(self):
        assert self.cls(1, 2)

    def test_invalid_class_args(self):
        with pytest.raises(TypeError):
            self.cls(1, 2, 3, 4)

    def test_restore(self):
        a = self.cls(x=1, y=2)
        assert a == self.cls.__restore__(json.loads(a.__json__()))

    def test_restore_obj(self):
        a = self.cls(x=1, y=2)
        assert a == self.cls.__restore__(a)

    def test_restore_optional(self):
        a = self.cls(x=1, y=None)
        assert a == self.cls.__restore__(a)

    def test_restore_normal(self):
        a = self.cls(x=1, y=None, z=1)
        assert a == self.cls.__restore__(a)

    def test_restore_invalid(self):
        with pytest.raises(ValidationError):
            self.cls.__restore__(object())

    def test_generate(self):
        a = self.cls.__generate__()
        assert a.x == 0
        assert a.y == 0
