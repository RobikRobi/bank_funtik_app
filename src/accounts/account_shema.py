from pydantic import BaseModel, Field

# схема для создания счёта
class AccountCreate(BaseModel):
    currency: str = Field(..., min_length=3, max_length=3)
    balance: float = Field(ge=0.0)

# схема для пополнения баланса счёта
class AccountUpdate(BaseModel):
    balance: float = Field(ge=0.0)