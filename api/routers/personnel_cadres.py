from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import PersonnelCadreSchema
from models import PersonnelCadre
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(personnel_cadre_id, db):
    personnel_cadre = (
        db.query(PersonnelCadre).filter(PersonnelCadre.id == personnel_cadre_id).first()
    )
    if personnel_cadre is None:
        raise HTTPException(
            status_code=404, detail=f"ID {personnel_cadre_id} : Does not exist"
        )

    return personnel_cadre


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_personnel_cadres(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_PERSONNEL_CADRE", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(PersonnelCadre)
        .filter(or_(PersonnelCadre.personnel_cadre.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(PersonnelCadre)
        .filter(or_(PersonnelCadre.personnel_cadre.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_personnel_cadre(
    personnel_cadre_schema: PersonnelCadreSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_PERSONNEL_CADRE", user["id"], db)
    personnel_cadre_model = PersonnelCadre()

    personnel_cadre_model.personnel_cadre = personnel_cadre_schema.personnel_cadre
    db.add(personnel_cadre_model)
    db.commit()
    return personnel_cadre_schema


@router.get("/{personnel_cadre_id}")
async def get_personnel_cadre(
    personnel_cadre_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_PERSONNEL_CADRE", user["id"], db)
    return get_object(personnel_cadre_id, db)


@router.put("/{personnel_cadre_id}")
async def update_personnel_cadre(
    personnel_cadre_id: int,
    personnel_cadre_schema: PersonnelCadreSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PERSONNEL_CADRE", user["id"], db)
    personnel_cadre_model = get_object(personnel_cadre_id, db)

    personnel_cadre_model.personnel_cadre = personnel_cadre_schema.personnel_cadre
    db.add(personnel_cadre_model)
    db.commit()

    return personnel_cadre_schema


@router.delete("/{personnel_cadre_id}")
async def delete_personnel_cadre(
    personnel_cadre_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PERSONNEL_CADRE", user["id"], db)
    get_object(personnel_cadre_id, db)
    db.query(PersonnelCadre).filter(PersonnelCadre.id == personnel_cadre_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Personnel Cadre Successfully deleted")
