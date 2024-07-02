from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import FinancialYearSchema
from models import FinancialYear
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(financial_year_id, db):
    financial_year = (
        db.query(FinancialYear).filter(FinancialYear.id == financial_year_id).first()
    )
    if financial_year is None:
        raise HTTPException(
            status_code=404, detail=f"ID {financial_year_id} : Does not exist"
        )
    return financial_year


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_financial_years(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_FINANCIAL_YEAR", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(FinancialYear)
        .filter(or_(FinancialYear.financial_year.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(FinancialYear)
        .filter(or_(FinancialYear.financial_year.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_financial_year(
    financial_year_schema: FinancialYearSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_FINANCIAL_YEAR", user["id"], db)

    if financial_year_schema.status == 1:
        db.query(FinancialYear).filter(FinancialYear.status == 1).update({"status": 0})
        db.commit()

    financial_year_model = FinancialYear(
        financial_year=financial_year_schema.financial_year,
        start_date=financial_year_schema.start_date,
        end_date=financial_year_schema.end_date,
        status=1 if financial_year_schema.status else 0,
    )

    db.add(financial_year_model)
    db.commit()

    return financial_year_schema


@router.get("/{financial_year_id}")
async def get_financial_year(
    financial_year_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_FINANCIAL_YEAR", user["id"], db)
    return get_object(financial_year_id, db)


@router.put("/{financial_year_id}")
async def update_financial_year(
    financial_year_id: int,
    financial_year_schema: FinancialYearSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_FINANCIAL_YEAR", user["id"], db)
    financial_year_model = get_object(financial_year_id, db)

    financial_year_model.financial_year = financial_year_schema.financial_year
    financial_year_model.start_date = financial_year_schema.start_date
    financial_year_model.end_date = financial_year_schema.end_date
    financial_year_model.status = financial_year_schema.status

    db.add(financial_year_model)
    db.commit()

    return financial_year_schema


@router.delete("/{financial_year_id}")
async def delete_financial_year(
    financial_year_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_FINANCIAL_YEAR", user["id"], db)
    get_object(financial_year_id, db)
    db.query(FinancialYear).filter(FinancialYear.id == financial_year_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="FinancialYear Successfully deleted")
