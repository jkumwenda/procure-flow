from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import DistrictSchema
from models import District
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


def get_object(district_id, db):
    district = db.query(District).filter(District.id == district_id).first()
    if district is None:
        raise HTTPException(
            status_code=404, detail=f"ID {district_id} : Does not exist"
        )
    return district


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_districts(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_DISTRICT", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(District)
        .filter(or_(District.district.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(District).filter(or_(District.district.ilike(f"%{search}%"))).count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_district(
    district_schema: DistrictSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_DISTRICT", user["id"], db)
    district_model = District(
        district=district_schema.district,
    )

    db.add(district_model)
    db.commit()

    return district_schema


@router.get("/{district_id}")
async def get_district(
    district_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_DISTRICT", user["id"], db)
    return get_object(district_id, db)


@router.put("/{district_id}")
async def update_district(
    district_id: int,
    district_schema: DistrictSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_DISTRICT", user["id"], db)
    district_model = get_object(district_id, db)

    district_model.district = (district_schema.district,)

    db.add(district_model)
    db.commit()
    return district_schema


@router.delete("/{district_id}")
async def delete_district(
    district_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_DISTRICT", user["id"], db)
    get_object(district_id, db)
    db.query(District).filter(District.id == district_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="District Successfully deleted")
