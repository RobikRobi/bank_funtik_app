from pydantic import BaseModel

class UserShow(BaseModel):
    id: int
    username: str
    password: str

