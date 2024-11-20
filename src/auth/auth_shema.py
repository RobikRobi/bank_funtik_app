from pydantic import BaseModel

class UserShow(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: str
    username: str
    # password: str

class UserUpdate(BaseModel):
    name: str=None
    surname: str=None
    phone: str=None
    password: str=None