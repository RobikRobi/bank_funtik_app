from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import select

from .auth_models import User
from ..database import get_session
from .auth_shema import UserUpdate, UserRegister, UserBase
from .auth_utils import creat_access_token, encode_password, check_password
from ..get_current_user import get_current_user

app = APIRouter(prefix="/users", tags=["Users"])

# регистрация пользователя
@app.post("/register")
def register_user(user_reg: UserRegister, session: Session = Depends(get_session)):
    h_password = encode_password(user_reg.password)
    user = User(email=user_reg.email, password=h_password, name=user_reg.name, surname=user_reg.surname,  phone=user_reg.phone)
    session.add(user)
    session.commit()
    return{"msg":"User registred successfully"}

# авторизация пользователя
@app.post("/login")
def login_user(email:str, password:str, session:Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.email == email))
    if user:
        if check_password(password, user.password):
            token = creat_access_token(user_id=int(user.id))
            return{"msg":"Login successful", "token":token}
    return{"msg":"Invalid username or password"}


# получение данных пользователя
@app.get("/me")
def get_me(user_data:User = Depends(get_current_user), session:Session = Depends(get_session)):
            return user_data

# измененние данных пользователя по id
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

# метод для пользователья с ролью администратор
def get_current_admin_user(current_user: UserBase = Depends(get_current_user), session: Session = Depends(get_session)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

# запрос на получение всех пользователей
@app.get("/all_users/")
def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return User.find_all()