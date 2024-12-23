from fastapi import FastAPI
from .database import engine, Base
from .auth.auth_router import app as auth_router
from .accounts.account_router import app as account_router
from .transactions.transaction_router import app as transaction_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)


@app.get("/")
def read_root():
    Base.metadata.create_all(engine)
    return{"Hello":"BankingAPP!"}