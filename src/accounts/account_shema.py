from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    currency: str = Field(..., min_length=3, max_length=3)
    balance: float = Field(ge=0.0)
    balance: float = Field(ge=0.0)

class AccountUpdate(BaseModel):
    balance: float = Field(ge=0.0)