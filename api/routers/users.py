import os
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
    status,
    File,
    UploadFile,
    Form,
)
from database import get_db
from sqlalchemy.orm import Session
from schemas.schemas import (
    UserRoleSchema,
    UserDepartmentSchema,
    UserPositionSchema,
    UserSchema,
    UserBaseSchema,
    UserResetPasswordSchema,
)
from models import Users, UserRole, UserDepartment, UserPosition, UserSignature
from dependencies import Security
import math
import uuid
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
import utils
from pydantic import EmailStr
from fastapi.responses import FileResponse
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter()


def get_object(user_id, db, model):
    query = db.query(model).filter(model.id == user_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    return query


@router.get("/")
async def get_users(
    # user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    # security.secureAccess("READ_USER", user["id"], db)

    offset = (skip - 1) * limit

    query = (
        db.query(Users)
        .filter(
            or_(
                Users.firstname.ilike(f"%{search}%"),
                Users.lastname.ilike(f"%{search}%"),
                Users.email.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Users)
        .filter(
            or_(
                Users.firstname.ilike(f"%{search}%"),
                Users.lastname.ilike(f"%{search}%"),
                Users.email.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_user(
    user_schema: UserSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_USER", user["id"], db)

    lowercase_email = user_schema.email.lower()
    existing_user = db.query(Users).filter(Users.email == lowercase_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Account with email {lowercase_email} already exists",
        )

    # Generate a random password if not provided or validate if provided
    if not user_schema.password:
        password = utils.generate_random_password()
    elif user_schema.password != user_schema.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    else:
        password = user_schema.password

    # Send a confirmation email (you can customize this part)
    utils.new_account_email(lowercase_email, user_schema.firstname, password)

    # Create the user model and add it to the database
    user_model = Users(
        email=lowercase_email,
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        phone=user_schema.phone,
        verified=True,
        password=utils.hash_password(password),
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return {"user_id": user_model.id}


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_base_schema: UserBaseSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_USER", user["id"], db)
    model = Users
    user_model = get_object(user_id, db, model)
    if user_base_schema.email != user_model.email:
        existing_user = (
            db.query(Users).filter(Users.email == user_base_schema.email).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email address {user_base_schema.email} is already in use",
            )
    user_model.firstname = user_base_schema.firstname
    user_model.lastname = user_base_schema.lastname
    user_model.phone = user_base_schema.phone
    user_model.email = user_base_schema.email

    db.add(user_model)
    db.commit()

    return user_base_schema


@router.put("/password/{user_id}")
async def update_password(
    user_id: int,
    # user: user_dependency,
    db: Session = Depends(get_db),
):
    # security.secureAccess("UPDATE_USER", user["id"], db)
    user = get_object(user_id, db, Users)
    password = utils.generate_random_password()

    db.query(Users).filter(Users.id == user_id).update(
        {"password": utils.hash_password(password)}
    )
    db.commit()
    # Send a confirmation email (you can customize this part)
    utils.password_change_email(user.email, user.firstname, password)
    raise HTTPException(status_code=200, detail="Password updated successfully")


@router.put("/reset_password/{user_id}")
async def reset_password(
    user_id: int,
    user: user_dependency,
    reset_password_schema: UserResetPasswordSchema,
    db: Session = Depends(get_db),
):
    # security.secureAccess("UPDATE_USER", user["id"], db)
    user = get_object(user_id, db, Users)
    password = reset_password_schema.password

    db.query(Users).filter(Users.id == user_id).update(
        {"password": utils.hash_password(reset_password_schema.password)}
    )
    db.commit()
    # Send a confirmation email (you can customize this part)
    utils.password_change_email(user.email, user.firstname, password)
    raise HTTPException(status_code=200, detail="Password updated successfully")


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_USER", user["id"], db)
    model = Users
    user = get_object(user_id, db, model)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "phone": user.phone,
        },
        "roles": [
            {
                "id": role.id,
                "role_id": role.role.id,
                "role": role.role.role,
            }
            for role in user.user_role
        ],
        "departments": [
            {
                "id": department.id,
                "department_id": department.department.id,
                "department": department.department.department,
            }
            for department in user.user_department
        ],
        "positions": [
            {
                "id": position.id,
                "position_id": position.position.id,
                "position": position.position.position,
            }
            for position in user.user_position
        ],
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)
    model = Users
    get_object(user_id, db, model)

    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Users Successfully deleted")


@router.get("/signatures/{user_id}")
async def get_user_signature(
    user_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_USER", user["id"], db)

    return db.query(UserSignature).filter(UserSignature.user_id == user_id).first()


@router.post("/signatures/")
async def add_user_signature(
    user: user_dependency,
    file: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_USER", user["id"], db)
    file_location = uuid.uuid4().hex
    os.mkdir(f"uploads/{file_location}")

    try:
        with open(f"uploads/{file_location}/{file.filename}", "wb") as f:
            f.write(file.file.read())
            user_signature_model = UserSignature(
                file_name=file.filename,
                user_id=user_id,
                file_size=0,
                file_type=file.content_type,
                file_location=(f"uploads/{file_location}/{file.filename}"),
            )

            db.add(user_signature_model)
            db.commit()
            db.refresh(user_signature_model)

            if user_signature_model.id is not None:
                return {
                    "id": user_signature_model.id,
                    "file_name": file.filename,
                    "user_id": user_id,
                    "file_type": file.content_type,
                    "file_location": (f"uploads/{file_location}"),
                }
        os.remove(file_location)
        raise HTTPException(
            status_code=404,
            detail="Signature creation in database failed, file deleted",
        )
    except Exception as e:
        return {"error": str(e)}


@router.get("/show_signatures/")
async def get_user_signature_image(file_location: str):
    security.secureAccess("READ_USER", id, db)
    try:
        return FileResponse(file_location)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image not found")


@router.delete("/signatures/{signature_id}")
async def delete_user_signature(
    signature_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)

    user_signature = (
        db.query(UserSignature).filter(UserSignature.id == signature_id).first()
    )
    try:
        os.remove(user_signature.file_location)
        db.query(UserSignature).filter(UserSignature.id == signature_id).delete()
        db.commit()
        raise HTTPException(
            status_code=200,
            detail=f"Signature {user_signature.file_location} removed successfully.",
        )
    except OSError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Error: {e}",
        )


@router.post("/roles/")
async def add_user_role(
    user_role_schema: UserRoleSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_USER", user["id"], db)
    user_role_model = UserRole(
        user_id=user_role_schema.user_id, role_id=user_role_schema.role_id
    )

    db.add(user_role_model)
    db.commit()
    db.refresh(user_role_model)
    return user_role_model


@router.put("/roles/{user_role_id}")
async def update_user_role(
    user_role_id: int,
    user_role_schema: UserRoleSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_USER", user["id"], db)
    user_role_model = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    user_role_model.user_id = (user_role_schema.user_id,)
    user_role_model.role_id = user_role_schema.role_id
    db.add(user_role_model)
    db.commit()
    db.refresh(user_role_model)
    return user_role_model


@router.delete("/roles/{user_role_id}")
async def delete_user_role(
    user_role_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)

    db.query(UserRole).filter(UserRole.id == user_role_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Users role successfully deleted")


@router.post("/departments/")
async def add_user_department(
    user_department_schema: UserDepartmentSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_USER", user["id"], db)
    user_department_model = UserDepartment(
        user_id=user_department_schema.user_id,
        department_id=user_department_schema.department_id,
    )
    db.add(user_department_model)
    db.commit()
    db.refresh(user_department_model)
    return user_department_model


@router.put("/departments/{user_department_id}")
async def update_user_department(
    user_department_schema: UserDepartmentSchema,
    user_department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_USER", user["id"], db)
    user_department_model = (
        db.query(UserDepartment).filter(UserDepartment.id == user_department_id).first()
    )
    user_department_model.user_id = (user_department_schema.user_id,)
    user_department_model.department_id = (user_department_schema.department_id,)

    db.add(user_department_model)
    db.commit()
    db.refresh(user_department_model)
    return user_department_model


@router.delete("/departments/{user_department_id}")
async def delete_user_department(
    user_department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)
    db.query(UserDepartment).filter(UserDepartment.id == user_department_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Users department successfully deleted")


@router.post("/positions/")
async def add_user_position(
    user_postion_schema: UserPositionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_USER", user["id"], db)
    user_position_model = UserPosition(
        user_id=user_postion_schema.user_id,
        position_id=user_postion_schema.position_id,
    )
    db.add(user_position_model)
    db.commit()
    db.refresh(user_position_model)
    return user_position_model


@router.put("/positions/{user_position_id}")
async def update_user_position(
    user_postion_schema: UserPositionSchema,
    user_position_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_USER", user["id"], db)
    user_position_model = (
        db.query(UserPosition).filter(UserPosition.id == user_position_id).first()
    )
    user_position_model.user_id = (user_postion_schema.user_id,)
    user_position_model.position_id = (user_postion_schema.position_id,)

    db.add(user_position_model)
    db.commit()
    db.refresh(user_position_model)
    return user_position_model


@router.delete("/positions/{user_position_id}")
async def delete_user_position(
    user_position_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)
    db.query(UserPosition).filter(UserPosition.id == user_position_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Users position successfully deleted")
