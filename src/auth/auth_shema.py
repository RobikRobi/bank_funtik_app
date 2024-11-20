from pydantic import BaseModel

class UserShow(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: str
    username: str
    # password: str

