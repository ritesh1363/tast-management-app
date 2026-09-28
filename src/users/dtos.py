from pydantic import BaseModel

class userschema(BaseModel):
    name:str
    username:str
    password:str
    email:str


class userresponseschema(BaseModel):
    id:int
    name:str
    username:str
    email:str


class login_schema(BaseModel):
    username:str
    password:str