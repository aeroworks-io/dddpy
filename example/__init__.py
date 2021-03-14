from faker import Faker

from dddpy import Entity, ID, Primitive


fake = Faker()
fake.seed_instance(0)


class UserID(ID):
    ...


class UserName(Primitive, str):
    """User's name"""

    @classmethod
    def __generate__(cls):
        return cls(fake.name())


class User(Entity):
    id: UserID
    name: UserName
