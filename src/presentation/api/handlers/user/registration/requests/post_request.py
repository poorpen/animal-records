from pydantic import BaseModel, Field


class AccountCreateVM(BaseModel):
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: str = Field(alias='email')
    password: str = Field(alias='password')
