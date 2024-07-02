from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import SupplierSchema, SupplierSupplierCategorySchema
from models import Supplier, SupplierSupplierCategory
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(id, db, model):
    query = db.query(model).filter(model.id == id).first()
    if query is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return query


router = APIRouter(
    responses={404: {"address": "Not found"}},
)


@router.get("/")
async def get_suppliers(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_SUPPLIER", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(Supplier)
        .filter(
            or_(
                Supplier.supplier.ilike(f"%{search}%"),
                Supplier.address.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Supplier)
        .filter(
            or_(
                Supplier.supplier.ilike(f"%{search}%"),
                Supplier.address.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_supplier(
    supplier_schema: SupplierSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_SUPPLIER", user["id"], db)
    supplier_model = Supplier(
        supplier=supplier_schema.supplier,
        address=supplier_schema.address,
        email=supplier_schema.email,
        phone=supplier_schema.phone,
    )

    db.add(supplier_model)
    db.commit()
    db.refresh(supplier_model)
    return supplier_model


@router.put("/{supplier_id}")
async def update_supplier(
    supplier_id: int,
    supplier_schema: SupplierSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_SUPPLIER", user["id"], db)
    model = Supplier
    supplier_model = get_object(supplier_id, db, model)

    supplier_model.supplier = supplier_schema.supplier
    supplier_model.address = supplier_schema.address
    supplier_model.email = supplier_schema.email
    supplier_model.phone = supplier_schema.phone
    db.add(supplier_model)
    db.commit()
    db.refresh(supplier_model)
    return supplier_model


@router.get("/{supplier_id}")
async def get_supplier(
    supplier_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_SUPPLIER", user["id"], db)
    supplier = get_object(supplier_id, db, Supplier)

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return {
        "supplier": {
            "id": supplier.id,
            "supplier": supplier.supplier,
            "address": supplier.address,
            "email": supplier.email,
            "phone": supplier.phone,
        },
        "supplier_categories": [
            {
                "id": supplier_category.id,
                "supplier_category_id": supplier_category.supplier_category.id,
                "supplier_category": supplier_category.supplier_category.supplier_category,
                "description": supplier_category.supplier_category.description,
            }
            for supplier_category in supplier.supplier_supplier_category
        ],
    }


@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_SUPPLIER", user["id"], db)
    model = Supplier
    get_object(supplier_id, db, model)

    db.query(Supplier).filter(Supplier.id == supplier_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Supplier Successfully deleted")


@router.post("/supplier_categories/")
async def add_supplier_supplier_category(
    supplier_supplier_category_schema: SupplierSupplierCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_SUPPLIER", user["id"], db)
    supplier_supplier_category_model = SupplierSupplierCategory(
        supplier_category_id=supplier_supplier_category_schema.supplier_category_id,
        supplier_id=supplier_supplier_category_schema.supplier_id,
    )
    db.add(supplier_supplier_category_model)
    db.commit()
    db.refresh(supplier_supplier_category_model)
    return supplier_supplier_category_model


@router.put("/supplier_categories/{supplier_supplier_category_id}")
async def update_supplier_supplier_category(
    supplier_supplier_category_id: int,
    supplier_supplier_category_schema: SupplierSupplierCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_SUPPLIER", user["id"], db)
    supplier_supplier_category_model = (
        db.query(SupplierSupplierCategory)
        .filter(SupplierSupplierCategory.id == supplier_supplier_category_id)
        .first()
    )
    supplier_supplier_category_model.supplier_category_id = (
        supplier_supplier_category_schema.supplier_category_id,
    )
    supplier_supplier_category_model.supplier_id = (
        supplier_supplier_category_schema.supplier_id,
    )

    db.add(supplier_supplier_category_model)
    db.commit()
    db.refresh(supplier_supplier_category_model)
    return supplier_supplier_category_model


@router.delete("/supplier_categories/{supplier_supplier_category_id}")
async def delete_supplier_supplier_category(
    supplier_supplier_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_SUPPLIER", user["id"], db)
    db.query(SupplierSupplierCategory).filter(
        SupplierSupplierCategory.id == supplier_supplier_category_id
    ).delete()
    db.commit()
    raise HTTPException(
        status_code=200, detail="Supplier category successfully deleted"
    )
