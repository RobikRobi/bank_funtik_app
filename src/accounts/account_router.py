from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .account_models import Account
from .account_shema import AccountCreate, AccountUpdate
from ..database import get_session
from ..auth.auth_models import User
from ..get_current_user import get_current_user


app = APIRouter(prefix="/accounts", tags=["Accounts"])

#создание счёта
@app.post("/")
def create_account(account_create: AccountCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    account = Account(owner_id=current_user.id, currency=account_create.currency, balance=account_create.balance)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

# получение сведений о всех счетах пользователя
@app.get("/")
def list_accounts(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    stmt = select(Account)
    accounts = session.query(Account).filter(Account.owner_id == current_user.id).all()
    return accounts

# получения данных о балансе определённого счёта
@app.get("/{account_id}/balance", response_model=float)
def get_balance(account_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    account = session.scalar(select(Account).filter(Account.id == account_id, Account.owner_id == current_user.id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.balance

# пополнение счёта
@app.put("/{account_id}/deposit")
def deposit_to_account(account_id: int, account_update: AccountUpdate, 
                       session: Session = Depends(get_session), 
                       current_user: User = Depends(get_current_user)):
    account = session.scalar(select(Account).filter(Account.id == account_id, Account.owner_id == current_user.id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance += account_update.balance
    session.commit()
    session.refresh(account)

    return {"message": f"Deposit of {account_update.balance} to account {account_id}"}

# удаление счёта
@app.delete("/{account_id}")
def close_account(account_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    account = session.scalar(select(Account).filter(Account.id == account_id, Account.owner_id == current_user.id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.balance != 0.0:
        raise HTTPException(status_code=400, detail="Account must have zero balance to be closed")
    session.delete(account)
    session.commit()
    return {"message": f"Account with ID {account_id} closed successfully"}

