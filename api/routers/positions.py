from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import PositionSchema
from models import Position
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(position_id, db):
    position = db.query(Position).filter(Position.id == position_id).first()
    if position is None:
        raise HTTPException(
            status_code=404, detail=f"ID {position_id} : Does not exist"
        )

    return position


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_positions(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    offset = (skip - 1) * limit
    query = (
        db.query(Position)
        .filter(or_(Position.position.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Position).filter(or_(Position.position.ilike(f"%{search}%"))).count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_position(
    position_schema: PositionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_POSITION", user["id"], db)
    position_model = Position()

    position_model.position = position_schema.position
    db.add(position_model)
    db.commit()
    return position_schema


@router.get("/{position_id}")
async def get_position(
    position_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_POSITION", user["id"], db)
    return get_object(position_id, db)


@router.put("/{position_id}")
async def update_position(
    position_id: int,
    position_schema: PositionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_POSITION", user["id"], db)
    position_model = get_object(position_id, db)

    position_model.position = position_schema.position
    db.add(position_model)
    db.commit()

    return position_schema


@router.delete("/{position_id}")
async def delete_position(
    position_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_POSITION", user["id"], db)
    get_object(position_id, db)
    db.query(Position).filter(Position.id == position_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Personnel Successfully deleted")
