from pydantic import BaseModel, Field


class SearchAccountParametersVM(BaseModel):
    first_name: str = Field(alias='firstName', default=" ")
    last_name: str = Field(alias='lastName', default=" ")
    email: str = Field(alias='email', default=" ")
    limit: int = Field(alias='size', default=10)
    offset: int = Field(default=0)
