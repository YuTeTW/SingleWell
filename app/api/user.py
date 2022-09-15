from fastapi import Depends, APIRouter, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.db.schemas import *
from app.db.database import get_db
from app.db import crud
from app import auth

router = APIRouter()


# create user
@router.post("/user", response_model=UserModel)
def create_user(user_data: UserCreateModel,
                db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_db = crud.create_user(db, user_data.email, user_data.password)
    return user_db


# login user
@router.post("/login", response_model=LoginResultModel)
def login(user_data: LoginModel,
          db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    result = auth.password_auth(db, user_data.email, user_data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Incorrect email or password", )
    else:
        access_token = authorize.create_access_token(subject=user_data.email,
                                                     expires_time=auth.ACCESS_TOKEN_EXPIRE_SECONDS)
        refresh_token = authorize.create_refresh_token(subject=user_data.email)
        return {"email": user_data.email, "token_type": "bearer", "access_token": access_token,
                "refresh_token": refresh_token}


# reset password
@router.patch("/user")
def reset_password(user_data: ResetModel,
                   db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    email = authorize.get_jwt_subject()
    result = auth.password_auth(db, email, user_data.old_password)
    if not result:
        raise HTTPException(status_code=401, detail="Incorrect old password", )
    crud.reset_password(db, email, user_data.new_password)
    return "Reset password success"
