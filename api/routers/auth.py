import os
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from models import Users, UserRole
from schemas.schemas import TokenSchema, UserSchema
from database import get_db
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

# Simulated token blacklist (you should use a database in a real-world scenario)
token_blacklist = set()


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_schema: UserSchema, db: Session = Depends(get_db)):
    create_user_model = Users(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        phone=user_schema.phone,
        email=user_schema.email,
        password=bcrypt.hash(user_schema.password),
        verified=1,
    )

    db.add(create_user_model)
    db.commit()

    return user_schema


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    user_response = get_user_response(user)

    permissions = get_user_permissions(db, user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response,
        "permissions": permissions,
    }


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_bearer),
):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        user_id: int = payload.get("id", 0)

        # Add the token to the blacklist
        token_blacklist.add(token)
        return {"message": "Logout successful"}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )


def authenticate_user(email: str, password: str, db):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        username: str = str(payload.get("sub"))
        user_id: int = int(payload.get("id", 0))
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


def get_user_response(user: Users) -> dict:
    return {
        "id": user.id,
        "phone": user.phone,
        "email": user.email,
        "verified": user.verified,
        "updated_at": user.updated_at,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "created_at": user.created_at,
    }


def get_user_permissions(db: Session, user_id: int) -> List[str]:
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    permissions = [
        rp.permission.permission_code
        for user_role in user_roles
        for rp in user_role.role.role_permission
    ]
    return permissions
