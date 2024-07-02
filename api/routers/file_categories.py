from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import FileCategorySchema
from models import FileCategory
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(file_category_id, db):
    file_category = (
        db.query(FileCategory).filter(FileCategory.id == file_category_id).first()
    )
    if file_category is None:
        raise HTTPException(
            status_code=404, detail=f"ID {file_category_id} : Does not exist"
        )

    return file_category


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_file_categories(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_FILE_CATEGORY", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(FileCategory)
        .filter(or_(FileCategory.file_category.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(FileCategory)
        .filter(or_(FileCategory.file_category.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_file_category(
    file_category_schema: FileCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_FILE_CATEGORY", user["id"], db)
    file_category_model = FileCategory()

    file_category_model.file_category = file_category_schema.file_category
    db.add(file_category_model)
    db.commit()
    return file_category_schema


@router.get("/{file_category_id}")
async def get_file_category(
    file_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_FILE_CATEGORY", user["id"], db)
    return get_object(file_category_id, db)


@router.put("/{file_category_id}")
async def update_file_category(
    file_category_id: int,
    file_category_schema: FileCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_FILE_CATEGORY", user["id"], db)
    file_category_model = get_object(file_category_id, db)

    file_category_model.file_category = file_category_schema.file_category
    db.add(file_category_model)
    db.commit()

    return file_category_schema


@router.delete("/{file_category_id}")
async def delete_file_category(
    file_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_FILE_CATEGORY", user["id"], db)
    get_object(file_category_id, db)
    db.query(FileCategory).filter(FileCategory.id == file_category_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="File Category Successfully deleted")
