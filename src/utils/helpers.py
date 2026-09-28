from fastapi import Request,HTTPException,status,Depends
from src.utils.settings import Settings
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db
import jwt
from src.users.models import user_model

def is_authenticated(request:Request,db:Session=Depends(get_db)):
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
