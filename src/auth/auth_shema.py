from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserShow(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: str
    username: str
    # password: str

class UserUpdate(BaseModel):
    name: str=None
    surname: str=None
    phone: str=None
    password: str=None


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    surname: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    phone: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")

    

    # @field_validator("phone_number")
    # # @classmethod
    # def validate_phone_number(cls, value: str) -> str:
    #     # if match(r'^\+\d{5,15}$', value):
    #         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
    #     return value