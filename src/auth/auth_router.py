from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from .auth_models import User
from ..database import get_session
from .auth_shema import UserShow
from .auth_utils import creat_access_token, decode_access_token

app = APIRouter()


@app.post("/register")
def register_user(username: str, password: str, session: Session = Depends(get_session)):
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return{"msg":"User registred successfully"}

@app.post("/login")
def login_user(username:str, password:str, session:Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.username == username, User.password == password))
    if user:
        token = creat_access_token(user_id=user.id)
        return{"msg":"Login successful", "token":token}
    else:
        return{"msg":"Invalid username or password"}
    
@app.get("/decode_token")
def decode_token(token:str):
    data = decode_access_token(token)
    return{"msg":"Token decode successfully", "data":data}


@app.get("/users", response_model=list[UserShow])
def read_users(session:Session = Depends(get_session)):
    users = session.scalars(select(User)).all()
    return users
