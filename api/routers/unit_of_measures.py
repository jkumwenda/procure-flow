from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import UnitOfMeasureSchema
from models import UnitOfMeasure
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(unit_of_measure_id, db):
    unit_of_measure = (
        db.query(UnitOfMeasure).filter(UnitOfMeasure.id == unit_of_measure_id).first()
    )
    if unit_of_measure is None:
        raise HTTPException(
            status_code=404, detail=f"ID {unit_of_measure_id} : Does not exist"
        )
    return unit_of_measure


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_unit_of_measures(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_UNIT_OF_MEASURE", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(UnitOfMeasure)
        .filter(or_(UnitOfMeasure.unit_of_measure.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(UnitOfMeasure)
        .filter(or_(UnitOfMeasure.unit_of_measure.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_unit_of_measure(
    unit_of_measure_schema: UnitOfMeasureSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_UNIT_OF_MEASURE", user["id"], db)

    unit_of_measure_model = UnitOfMeasure(
        unit_of_measure=unit_of_measure_schema.unit_of_measure
    )

    db.add(unit_of_measure_model)
    db.commit()

    return unit_of_measure_schema


@router.get("/{unit_of_measure_id}")
async def get_unit_of_measure(
    unit_of_measure_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_UNIT_OF_MEASURE", user["id"], db)
    return get_object(unit_of_measure_id, db)


@router.put("/{unit_of_measure_id}")
async def update_unit_of_measure(
    unit_of_measure_id: int,
    unit_of_measure_schema: UnitOfMeasureSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_UNIT_OF_MEASURE", user["id"], db)
    unit_of_measure_model = get_object(unit_of_measure_id, db)

    unit_of_measure_model.unit_of_measure = unit_of_measure_schema.unit_of_measure
    db.add(unit_of_measure_model)
    db.commit()

    return unit_of_measure_schema


@router.delete("/{unit_of_measure_id}")
async def delete_unit_of_measure(
    unit_of_measure_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_UNIT_OF_MEASURE", user["id"], db)
    get_object(unit_of_measure_id, db)
    db.query(UnitOfMeasure).filter(UnitOfMeasure.id == unit_of_measure_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Unit of measure successfully deleted")
