from fastapi import HTTPException,status,Request,BackgroundTasks
from src.users.dtos import userschema,login_schema
from src.utils.settings import Settings
from sqlalchemy.orm import Session
from src.users.models import user_model
from datetime import datetime,timedelta
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_mail

##this object is to hash the password
password_hash=PasswordHash.recommended()

def get_password_hash(password):
        return password_hash.hash(password)

##to verify the login password
def verify_password(plain_password,hashed_password):
     return password_hash.verify(plain_password,hashed_password)

async def register(body:userschema,db:Session,bg_task:BackgroundTasks):
    ## for removing the duplicacy of the username and email
    is_user=db.query(user_model).filter(user_model.username==body.username).first()
    if is_user:
        raise HTTPException(400,detail="username already exixt..")
    
    is_user=db.query(user_model).filter(user_model.email==body.email).first()
    if is_user:
        raise HTTPException(400,detail="email already exixt..")

    ## for hashing the password
    hash_password=get_password_hash(body.password)

    ##creating the object of user_model
    new_user=user_model(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email
    )

    ## now to add our user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    ##send email to user for confirmation of registration
    bg_task.add_task(send_mail,[new_user.email])

    return new_user 


def login_user(body:login_schema,db:Session):
    user=db.query(user_model).filter(user_model.username==body.username).first()
    ##for verification of username
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="wrong username!")
    ## for verification of password
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="wrong password!")
    ## for efficient login of user using jwt tokens
    exp_time= datetime.now()+timedelta(minutes=Settings.EXP_TIME)

    token=jwt.encode({"_id":user.id,"exp":exp_time.timestamp()},Settings.SECRET_KEY,Settings.ALGORITHM)

    return {"token":token}


##token based authentication
def is_authenticated(request:Request,db:Session):
    try:
        token=request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are unauthorised")
             
        token=token.split(" ")[-1]
         
        data=jwt.decode(token,Settings.SECRET_KEY,Settings.ALGORITHM)
        user_id=data.get("_id")
             
        user=db.query(user_model).filter(user_model.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are unauthorised")
         
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are unauthorised")
    