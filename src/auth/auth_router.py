from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from sqlalchemy.orm import Session

from .auth_models import User
from ..database import get_session

app = APIRouter()

@app.post("/register")
def register_user(username: str, password: str, sessionmaker: Session = Depends(get_session)):
    user = User(username=username, password=password)
    Session.add(user)
    Session.commit()
    return{"msg":"User registred succesfully"}
