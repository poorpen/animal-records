from pydantic import BaseModel, Field


class SearchAccountParametersVM(BaseModel):
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: str = Field(alias='email')
    offset: int = Field(alias='from', default=0)
    limit: int = Field(alias='size', default=10)
