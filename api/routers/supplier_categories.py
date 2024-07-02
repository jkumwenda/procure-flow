from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import SupplierCategorySchema
from models import SupplierCategory
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(supplier_category_id, db):
    supplier_category = (
        db.query(SupplierCategory)
        .filter(SupplierCategory.id == supplier_category_id)
        .first()
    )
    if supplier_category is None:
        raise HTTPException(
            status_code=404, detail=f"ID {supplier_category_id} : Does not exist"
        )
    return supplier_category


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_supplier_categories(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_SUPPLIER_CATEGORY", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(SupplierCategory)
        .filter(or_(SupplierCategory.supplier_category.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(SupplierCategory)
        .filter(or_(SupplierCategory.supplier_category.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_supplier_category(
    supplier_category_schema: SupplierCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_SUPPLIER_CATEGORY", user["id"], db)

    supplier_category_model = SupplierCategory(
        supplier_category=supplier_category_schema.supplier_category,
        description=supplier_category_schema.description,
    )

    db.add(supplier_category_model)
    db.commit()

    return supplier_category_schema


@router.get("/{supplier_category_id}")
async def get_supplier_category(
    supplier_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_SUPPLIER_CATEGORY", user["id"], db)
    return get_object(supplier_category_id, db)


@router.put("/{supplier_category_id}")
async def update_supplier_category(
    supplier_category_id: int,
    supplier_category_schema: SupplierCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_SUPPLIER_CATEGORY", user["id"], db)
    supplier_category_model = get_object(supplier_category_id, db)

    supplier_category_model.supplier_category = (
        supplier_category_schema.supplier_category
    )
    supplier_category_model.description = supplier_category_schema.description
    db.add(supplier_category_model)
    db.commit()

    return supplier_category_schema


@router.delete("/{supplier_category_id}")
async def delete_supplier_category(
    supplier_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_SUPPLIER_CATEGORY", user["id"], db)
    get_object(supplier_category_id, db)
    db.query(SupplierCategory).filter(
        SupplierCategory.id == supplier_category_id
    ).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Unit of measure successfully deleted")
