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
    email: EmailStr = Field(..., description="e-mail")
    password: str = Field(..., min_length=5, max_length=50, description="Password, from 5 to 50 characters")
    name: str = Field(..., min_length=3, max_length=50, description="Name, from 3 to 50 characters")
    surname: str = Field(..., min_length=3, max_length=50, description="Last name, from 3 to 50 characters")
    phone: str = Field(..., description="Phone number in international format starting with '+'")

    

    # @field_validator("phone_number")
    # # @classmethod
    # def validate_phone_number(cls, value: str) -> str:
    #     # if match(r'^\+\d{5,15}$', value):
    #         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
    #     return value