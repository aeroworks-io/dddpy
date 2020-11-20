from dddpy import Entity, ID, Value, Field


class UserID(ID):
    ...


class UserName(Value):
    value: str = Field(..., description="User's name")


class User(Entity):
    id: UserID
    name: UserName
