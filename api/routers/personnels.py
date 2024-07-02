import os
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Query
from schemas.schemas import PersonnelSchema
from models import (
    Personnel,
    District,
    PersonnelCadre,
    PersonnelFile,
    FileCategory,
)
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
import uuid
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(personnel_id, db):
    personnel = db.query(Personnel).filter(Personnel.id == personnel_id).first()
    if personnel is None:
        raise HTTPException(
            status_code=404, detail=f"ID {personnel_id} : Does not exist"
        )

    return personnel


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_business_entities(
    department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_BUSINESS_ENTITY", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(Personnel)
        .join(PersonnelCadre, Personnel.personnel_cadre_id == PersonnelCadre.id)
        .filter(
            or_(
                Personnel.firstname.ilike(f"%{search}%"),
                Personnel.lastname.ilike(f"%{search}%"),
                Personnel.reg_number.ilike(f"%{search}%"),
                Personnel.email.ilike(f"%{search}%"),
                Personnel.phone.ilike(f"%{search}%"),
                PersonnelCadre.personnel_cadre.ilike(f"%{search}%"),
            ),
        )
        .options(
            joinedload(Personnel.personnel_cadre),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Personnel)
        .join(PersonnelCadre, Personnel.personnel_cadre_id == PersonnelCadre.id)
        .filter(
            or_(
                Personnel.firstname.ilike(f"%{search}%"),
                Personnel.lastname.ilike(f"%{search}%"),
                Personnel.reg_number.ilike(f"%{search}%"),
                Personnel.email.ilike(f"%{search}%"),
                Personnel.phone.ilike(f"%{search}%"),
                PersonnelCadre.personnel_cadre.ilike(f"%{search}%"),
            ),
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_personnel(
    personnel_schema: PersonnelSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_BUSINESS_ENTITY", user["id"], db)
    personnel_model = Personnel(
        firstname=personnel_schema.firstname,
        lastname=personnel_schema.lastname,
        reg_number=personnel_schema.reg_number,
        personnel_cadre_id=personnel_schema.personnel_cadre_id,
        email=personnel_schema.email,
        phone=personnel_schema.phone,
    )
    db.add(personnel_model)
    db.commit()
    return personnel_schema


@router.get("/{personnel_id}")
async def get_personnel(
    personnel_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_PERMISSION", user["id"], db)
    return get_object(personnel_id, db)


@router.get("/personnel_files/{personnel_id}")
async def get_personnel_records(
    personnel_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_BUSINESS_ENTITY", user["id"], db)
    personnel = get_object(personnel_id, db)

    personnel = (
        db.query(Personnel)
        .join(PersonnelCadre, Personnel.personnel_cadre_id == PersonnelCadre.id)
        .filter(Personnel.id == personnel_id)
        .options(
            joinedload(Personnel.personnel_cadre),
        )
        .first()
    )

    if not personnel:
        raise HTTPException(status_code=404, detail="Business entity not found")

    offset = (skip - 1) * limit
    query = (
        db.query(PersonnelFile)
        .filter(PersonnelFile.personnel_id == personnel_id)
        .join(FileCategory, PersonnelFile.file_category_id == FileCategory.id)
        .filter(
            or_(
                PersonnelFile.file_name.ilike(f"%{search}%"),
                PersonnelFile.real_file_name.ilike(f"%{search}%"),
                FileCategory.file_category.ilike(f"%{search}%"),
            )
        )
        .options(joinedload(PersonnelFile.file_category))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_count = (
        db.query(PersonnelFile)
        .join(FileCategory, PersonnelFile.file_category_id == FileCategory.id)
        .filter(
            or_(
                PersonnelFile.file_name.ilike(f"%{search}%"),
                PersonnelFile.real_file_name.ilike(f"%{search}%"),
                FileCategory.file_category.ilike(f"%{search}%"),
            )
        )
        .filter(PersonnelFile.personnel_id == personnel_id)
        .count()
    )

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "personnel": personnel, "data": query}


@router.put("/{personnel_id}")
async def update_personnel(
    personnel_id: int,
    personnel_schema: PersonnelSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_BUSINESS_ENTITY", user["id"], db)
    personnel_model = get_object(personnel_id, db)

    personnel_model.firstname = personnel_schema.firstname
    personnel_model.lastname = personnel_schema.lastname
    personnel_model.reg_number = personnel_schema.reg_number
    personnel_model.personnel_cadre_id = personnel_schema.personnel_cadre_id
    personnel_model.email = personnel_schema.email
    personnel_model.phone = personnel_schema.phone

    db.add(personnel_model)
    db.commit()
    return personnel_schema


@router.delete("/{personnel_id}")
async def delete_personnel(
    personnel_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BUSINESS_ENTITY", user["id"], db)
    get_object(personnel_id, db)
    db.query(Personnel).filter(Personnel.id == personnel_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Business Entity Successfully deleted")


@router.post("/upload_personnel_file/")
async def add_personnel_record(
    user: user_dependency,
    file: UploadFile = File(...),
    file_category_id=File(...),
    personnel_id: int = Form(...),
    file_name: str = Form(...),
    access_level: str = Form(...),
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_REQUEST", user["id"], db)

    file_location = uuid.uuid4().hex
    os.mkdir(f"uploads/{file_location}")

    try:
        with open(f"uploads/{file_location}/{file.filename}", "wb") as f:
            f.write(file.file.read())
            personnel_model = PersonnelFile(
                file_name=file_name,
                real_file_name=file.filename,
                file_category_id=file_category_id,
                personnel_id=personnel_id,
                access_level=access_level,
                file_size=0,
                file_type=file.content_type,
                file_location=(f"uploads/{file_location}/{file.filename}"),
            )

            db.add(personnel_model)
            db.commit()
            db.refresh(personnel_model)

            if personnel_model.id is not None:
                return {
                    "id": personnel_model.id,
                    "file_name": file.filename,
                    "real_file_name": file.filename,
                    "file_category_id": file_category_id,
                    "personnel_id": personnel_id,
                    "access_level": access_level,
                    "file_type": file.content_type,
                    "file_location": (f"uploads/{file_location}"),
                }
        os.remove(file_location)
        raise HTTPException(
            status_code=404, detail="File creation in database failed, file deleted"
        )
    except Exception as e:
        return {"error": str(e)}


@router.delete("/delete_personnel_file/{personnel_file_id}")
async def delete_personnel_file(
    personnel_file_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    # security.secureAccess("DELETE_DEPARTMENT_FILE", user["id"], db)
    personnel = (
        db.query(PersonnelFile).filter(PersonnelFile.id == personnel_file_id).first()
    )
    os.remove(personnel.file_location)
    db.query(PersonnelFile).filter(PersonnelFile.id == personnel_file_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail=f"Department file Successfully deleted")
