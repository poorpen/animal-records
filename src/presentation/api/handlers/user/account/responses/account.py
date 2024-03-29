from typing import List

from pydantic import BaseModel, Field


class AccountVM(BaseModel):
    id: int = Field(alias='id')
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: str = Field(alias='email')

    class Config:
        allow_population_by_field_name = True


class AccountsVM(BaseModel):
    accounts: List[AccountVM]
