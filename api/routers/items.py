from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import ItemSchema
from models import Item
from dependencies import Security
from database import get_db
import math
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(item_id, db):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"ID {item_id} : Does not exist")
    return item


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_items(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_ITEM", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(Item)
        .filter(or_(Item.item.ilike(f"%{search}%")))
        .options(joinedload(Item.unit_of_measure))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Item)
        .filter(or_(Item.item.ilike(f"%{search}%")))
        .options(joinedload(Item.unit_of_measure))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_item(
    item_schema: ItemSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_ITEM", user["id"], db)

    item_model = Item(
        item=item_schema.item, unit_of_measure_id=item_schema.unit_of_measure_id
    )

    db.add(item_model)
    db.commit()

    return item_schema


@router.get("/{item_id}")
async def get_item(
    item_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_ITEM", user["id"], db)
    return get_object(item_id, db)


@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item_schema: ItemSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_ITEM", user["id"], db)
    item_model = get_object(item_id, db)

    item_model.item = item_schema.item
    item_model.unit_of_measure_id = item_schema.unit_of_measure_id

    db.add(item_model)
    db.commit()

    return item_schema


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_ITEM", user["id"], db)
    get_object(item_id, db)
    db.query(Item).filter(Item.id == item_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Item Successfully deleted")
