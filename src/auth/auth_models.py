from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    
    def __init__(self,username, password):
        self.username = username
        self.password = password
      