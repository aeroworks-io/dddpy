from unittest.case import TestCase
import toml

import dddpy


class MetaTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open('pyproject.toml') as pyproject:
            self.pyproject = toml.load(pyproject)

    def test_versions(self):
        assert self.pyproject['tool']['poetry']['version'] == dddpy.__version__
