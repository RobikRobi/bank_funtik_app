from fastapi import FastAPI
from .database import engine, Base
from .auth.auth_router import app as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def read_root():
    Base.metadata.create_all(engine)
    return{"Hello":"BankingAPP!"}