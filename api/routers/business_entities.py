import os
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Query
from schemas.schemas import BusinessEntitySchema
from models import (
    BusinessEntity,
    District,
    BusinessCategory,
    BusinessEntityFile,
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


def get_object(business_entity_id, db):
    business_entity = (
        db.query(BusinessEntity).filter(BusinessEntity.id == business_entity_id).first()
    )
    if business_entity is None:
        raise HTTPException(
            status_code=404, detail=f"ID {business_entity_id} : Does not exist"
        )

    return business_entity


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_business_entities(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_BUSINESS_ENTITY", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(BusinessEntity)
        .join(District, BusinessEntity.district_id == District.id)
        .join(
            BusinessCategory, BusinessEntity.business_category_id == BusinessCategory.id
        )
        .filter(
            or_(
                BusinessEntity.business_name.ilike(f"%{search}%"),
                District.district.ilike(f"%{search}%"),
                BusinessCategory.business_category.ilike(f"%{search}%"),
            ),
        )
        .options(
            joinedload(BusinessEntity.district),
            joinedload(BusinessEntity.business_category),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(BusinessEntity)
        .join(District, BusinessEntity.district_id == District.id)
        .join(
            BusinessCategory, BusinessEntity.business_category_id == BusinessCategory.id
        )
        .filter(
            or_(
                BusinessEntity.business_name.ilike(f"%{search}%"),
                District.district.ilike(f"%{search}%"),
                BusinessCategory.business_category.ilike(f"%{search}%"),
            ),
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_business_entity(
    business_entity_schema: BusinessEntitySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_BUSINESS_ENTITY", user["id"], db)
    business_entity_model = BusinessEntity(
        business_name=business_entity_schema.business_name,
        district_id=business_entity_schema.district_id,
        business_category_id=business_entity_schema.business_category_id,
        address=business_entity_schema.address,
        email=business_entity_schema.email,
        phone=business_entity_schema.phone,
    )
    db.add(business_entity_model)
    db.commit()
    return business_entity_schema


@router.get("/business_entity_files/{business_entity_id}")
async def get_business_entity_records(
    business_entity_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_BUSINESS_ENTITY", user["id"], db)
    business_entity = get_object(business_entity_id, db)

    business_entity = (
        db.query(BusinessEntity)
        .join(District, BusinessEntity.district_id == District.id)
        .join(
            BusinessCategory, BusinessEntity.business_category_id == BusinessCategory.id
        )
        .filter(BusinessEntity.id == business_entity_id)
        .options(
            joinedload(BusinessEntity.district),
            joinedload(BusinessEntity.business_category),
        )
        .first()
    )

    if not business_entity:
        raise HTTPException(status_code=404, detail="Business entity not found")

    offset = (skip - 1) * limit
    query = (
        db.query(BusinessEntityFile)
        .filter(BusinessEntityFile.business_entity_id == business_entity_id)
        .join(FileCategory, BusinessEntityFile.file_category_id == FileCategory.id)
        .filter(
            or_(
                BusinessEntityFile.file_name.ilike(f"%{search}%"),
                BusinessEntityFile.real_file_name.ilike(f"%{search}%"),
                FileCategory.file_category.ilike(f"%{search}%"),
            )
        )
        .options(joinedload(BusinessEntityFile.file_category))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_count = (
        db.query(BusinessEntityFile)
        .join(FileCategory, BusinessEntityFile.file_category_id == FileCategory.id)
        .filter(
            or_(
                BusinessEntityFile.file_name.ilike(f"%{search}%"),
                BusinessEntityFile.real_file_name.ilike(f"%{search}%"),
                FileCategory.file_category.ilike(f"%{search}%"),
            )
        )
        .filter(BusinessEntityFile.business_entity_id == business_entity_id)
        .count()
    )

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "business_entity": business_entity, "data": query}


@router.get("/{business_entity_id}")
async def get_business_entity(
    business_entity_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_PERMISSION", user["id"], db)
    return get_object(business_entity_id, db)


@router.put("/{business_entity_id}")
async def update_business_entity(
    business_entity_id: int,
    business_entity_schema: BusinessEntitySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_BUSINESS_ENTITY", user["id"], db)
    business_entity_model = get_object(business_entity_id, db)

    business_entity_model.business_name = business_entity_schema.business_name
    business_entity_model.district_id = business_entity_schema.district_id
    business_entity_model.business_category_id = (
        business_entity_schema.business_category_id
    )
    business_entity_model.address = business_entity_schema.address
    business_entity_model.email = business_entity_schema.email
    business_entity_model.phone = business_entity_schema.phone
    db.add(business_entity_model)
    db.commit()
    return business_entity_schema


@router.delete("/{business_entity_id}")
async def delete_business_entity(
    business_entity_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BUSINESS_ENTITY", user["id"], db)
    get_object(business_entity_id, db)
    db.query(BusinessEntity).filter(BusinessEntity.id == business_entity_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Business Entity Successfully deleted")


@router.post("/upload_business_entity_file/")
async def add_business_entity_record(
    user: user_dependency,
    file: UploadFile = File(...),
    file_category_id=File(...),
    business_entity_id: int = Form(...),
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
            business_entity_model = BusinessEntityFile(
                file_name=file_name,
                real_file_name=file.filename,
                file_category_id=file_category_id,
                business_entity_id=business_entity_id,
                access_level=access_level,
                file_size=0,
                file_type=file.content_type,
                file_location=(f"uploads/{file_location}/{file.filename}"),
            )

            db.add(business_entity_model)
            db.commit()
            db.refresh(business_entity_model)

            if business_entity_model.id is not None:
                return {
                    "id": business_entity_model.id,
                    "file_name": file.filename,
                    "real_file_name": file.filename,
                    "file_category_id": file_category_id,
                    "business_entity_id": business_entity_id,
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


@router.delete("/delete_business_entity_file/{business_entity_file_id}")
async def delete_business_entity_file(
    business_entity_file_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BUSINESS_ENTITY", user["id"], db)
    business_entity = (
        db.query(BusinessEntityFile)
        .filter(BusinessEntityFile.id == business_entity_file_id)
        .first()
    )
    os.remove(business_entity.file_location)
    db.query(BusinessEntityFile).filter(
        BusinessEntityFile.id == business_entity_file_id
    ).delete()
    db.commit()

    raise HTTPException(status_code=200, detail=f"Department file Successfully deleted")
