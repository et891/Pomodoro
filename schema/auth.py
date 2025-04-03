from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id:int
    email:str
    verified_email:bool
    name:str
    access_token:str

class YandexUserData(BaseModel):
    id:int
    login:str
    name:str = Field(None, alias="real_name")
    default_email:str
    access_token:str