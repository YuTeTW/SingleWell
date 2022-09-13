from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class LoginResultModel(UserBase):
    email: EmailStr
    token_type: str
    access_token: str
    refresh_token: str


class LoginModel(UserBase):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "dave@fastwise.net",
                "password": "dave"
            }
        }


class UserCreateModel(UserBase):
    email: EmailStr
    password: str


class UserModel(UserBase):
    id: int
    email: EmailStr
    password: str


class ResetModel(UserBase):
    old_password: str
    new_password: str
