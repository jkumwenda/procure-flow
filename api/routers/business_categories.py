from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import BusinessCategorySchema
from models import BusinessCategory
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(business_category_id, db):
    business_category = (
        db.query(BusinessCategory)
        .filter(BusinessCategory.id == business_category_id)
        .first()
    )
    if business_category is None:
        raise HTTPException(
            status_code=404, detail=f"ID {business_category_id} : Does not exist"
        )

    return business_category


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_business_categories(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_BUSINESS_CATEGORY", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(BusinessCategory)
        .filter(or_(BusinessCategory.business_category.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(BusinessCategory)
        .filter(or_(BusinessCategory.business_category.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_business_category(
    business_category_schema: BusinessCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_BUSINESS_CATEGORY", user["id"], db)
    business_category_model = BusinessCategory()

    business_category_model.business_category = (
        business_category_schema.business_category
    )
    db.add(business_category_model)
    db.commit()
    return business_category_schema


@router.get("/{business_category_id}")
async def get_business_category(
    business_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_BUSINESS_CATEGORY", user["id"], db)
    return get_object(business_category_id, db)


@router.put("/{business_category_id}")
async def update_business_category(
    business_category_id: int,
    business_category_schema: BusinessCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_BUSINESS_CATEGORY", user["id"], db)
    business_category_model = get_object(business_category_id, db)

    business_category_model.business_category = (
        business_category_schema.business_category
    )
    db.add(business_category_model)
    db.commit()

    return business_category_schema


@router.delete("/{business_category_id}")
async def delete_business_category(
    business_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BUSINESS_CATEGORY", user["id"], db)
    get_object(business_category_id, db)
    db.query(BusinessCategory).filter(
        BusinessCategory.id == business_category_id
    ).delete()
    db.commit()

    raise HTTPException(
        status_code=200, detail="Business Category Successfully deleted"
    )
