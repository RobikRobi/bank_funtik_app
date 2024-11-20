from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from .auth_models import User
from ..database import get_session
from .auth_shema import UserShow, UserUpdate
from .auth_utils import creat_access_token, valid_access_token, encode_password, check_password
from ..get_current_user import get_current_user, get_current_id

app = APIRouter(prefix="/users", tags=["Users"])


@app.post("/register")
def register_user(name: str, surname: str, email: str, phone: str, password: str, session: Session = Depends(get_session)):
    h_password = encode_password(password)
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


@app.get("/me")
def get_me(user_data:User = Depends(get_current_user), session:Session = Depends(get_session)):
            return user_data

@app.put("/{user_id}")
def user_update(user_id: int, user_update: UserUpdate, session:Session = Depends(get_session)):
    user = session.scalar(select(User).filter(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.surname is not None:
        user.surname = user_update.surname
    if user_update.phone is not None:
        user.phone = user_update.phone
    if user_update.password is not None:
        user.password_hash = encode_password(user_update.password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": f"User with ID {user_id} updated successfully"}