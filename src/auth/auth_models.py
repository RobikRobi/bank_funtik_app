from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    username: Mapped[str]
    password: Mapped[bytes]

    # is_user:Mapped[bool] = mapped_column(default=True, nullable=False )
    # is_admin:Mapped[bool] = mapped_column(default=False, nullable=False)

    # extend_existing = True
    
    def __init__(self, name, surname, email, phone, username, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
      