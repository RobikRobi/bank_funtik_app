from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Mapped[int], mapped_column(primary_key=True)
    sender_account_id = Mapped[int], mapped_column (ForeignKey('accounts.id'), nullable=False)
    recipient_account_id = Mapped[int], mapped_column(ForeignKey('accounts.id'))
    amount = Mapped[float], mapped_column(nullable=False)
    description = Mapped[str]
    transaction_date = Mapped[DateTime], mapped_column(default=datetime.now)

    sender = relationship("Account", foreign_keys=[sender_account_id], backref='sent_transactions')
    recipient = relationship("Account", foreign_keys=[recipient_account_id], backref='received_transactions')