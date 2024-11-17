from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from .auth_models import User
from ..database import get_session
from .auth_shema import UserShow
from .auth_utils import creat_access_token, valid_access_token, decode_password, check_password
from ..get_current_user import get_current_user

app = APIRouter()


@app.post("/register")
def register_user(name: str, surname: str, email: str, phone: str, password: str, session: Session = Depends(get_session)):
    h_password = decode_password(password)
    user = User(name=name, surname=surname, email=email, phone=phone, username=email, password=h_password)
    session.add(user)
    session.commit()
    return{"msg":"User registred successfully"}

@app.post("/login")
def login_user(username:str, password:str, session:Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.username == username))
    if user:
        if check_password(password, user.password):
            token = creat_access_token(user_id=int(user.id))
            return{"msg":"Login successful", "token":token}
    return{"msg":"Invalid username or password"}
    
@app.get("/decode_token")
def decode_token(token:str):
    data = valid_access_token(token)
    return{"msg":"Token decode successfully", "data":data}


@app.get("/users", response_model=list[UserShow])
def read_users(user:User = Depends(get_current_user), session:Session = Depends(get_session)):

            users = session.scalars(select(User)).all()
            return users
