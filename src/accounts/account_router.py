from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .account_models import Account
from .account_shema import AccountCreate
from ..database import get_session
from ..auth.auth_models import User
from ..get_current_user import get_current_user
from typing import List

app = APIRouter(prefix="/accounts", tags=["Accounts"])

# , response_model=Account
@app.post("/")
def create_account(account_create: AccountCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    account = Account(owner_id=current_user.id, currency=account_create.currency)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

@app.get("/")
def list_accounts(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    accounts = session.query(Account).filter(Account.owner_id == current_user.id).all()
    return accounts

@app.get("/{account_id}/balance", response_model=float)
def get_balance(account_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    account = session.query(Account).filter(Account.id == account_id, Account.owner_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.balance

@app.delete("/{account_id}")
def close_account(account_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    account = session.query(Account).filter(Account.id == account_id, Account.owner_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.balance != 0.0:
        raise HTTPException(status_code=400, detail="Account must have zero balance to be closed")
    session.delete(account)
    session.commit()
    return {"message": f"Account with ID {account_id} closed successfully"}