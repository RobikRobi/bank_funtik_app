from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Mapped[int], mapped_column (primary_key=True)
    owner_id = Mapped[int], ForeignKey('users.id')
    currency = Mapped[str], mapped_column(nullable=False)
    balance = Mapped[float], mapped_column(default=0.0)

    owner = relationship("User", back_populates="accounts")

