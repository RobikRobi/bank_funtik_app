from pydantic import BaseModel, EmailStr, Field, field_validator
import re

# схема для обновления данных о пользователе
class UserUpdate(BaseModel):
    name: str=None
    surname: str=None
    phone: str=None
    password: str=None

class UserBase(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    phone: str

    is_user: bool
    Is_admin: bool

    

# схема для регистрации пользователя
class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="e-mail")
    password: str = Field(..., min_length=5, max_length=50, description="Password, from 5 to 50 characters")
    name: str = Field(..., min_length=3, max_length=50, description="Name, from 3 to 50 characters")
    surname: str = Field(..., min_length=3, max_length=50, description="Last name, from 3 to 50 characters")
    phone: str = Field(..., description="Phone number in international format starting with '+'")

    
# валидация номера телефона
    @field_validator("phone")
    def validate_phone_number(value: str) -> str:
        if value[0] != '+':
            raise ValueError('The phone number must start with "+"')
        if len(value) != 12:
            raise ValueError('Phone number must contain 11 digits')
        return value