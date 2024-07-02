from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import BudgetSchema
from models import Budget
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


def get_object(budget_id, db):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=404, detail=f"ID {budget_id} : Does not exist")
    return budget


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_budgets(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_BUDGET", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(Budget)
        .filter(or_(Budget.amount.ilike(f"%{search}%")))
        .options(joinedload(Budget.financial_year), joinedload(Budget.department))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Budget)
        .filter(or_(Budget.amount.ilike(f"%{search}%")))
        .options(joinedload(Budget.financial_year), joinedload(Budget.department))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_budget(
    budget_schema: BudgetSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_BUDGET", user["id"], db)

    budget_model = Budget(
        amount=budget_schema.amount,
        department_id=budget_schema.department_id,
        financial_year_id=budget_schema.financial_year_id,
    )

    db.add(budget_model)
    db.commit()

    return budget_schema


@router.get("/{budget_id}")
async def get_budget(
    budget_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_BUDGET", user["id"], db)
    return get_object(budget_id, db)


@router.put("/{budget_id}")
async def update_budget(
    budget_id: int,
    budget_schema: BudgetSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_BUDGET", user["id"], db)
    budget_model = get_object(budget_id, db)

    budget_model.amount = budget_schema.amount
    budget_model.department_id = budget_schema.department_id
    budget_model.financial_year_id = budget_schema.financial_year_id

    db.add(budget_model)
    db.commit()

    return budget_schema


@router.delete("/{budget_id}")
async def delete_budget(
    budget_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BUDGET", user["id"], db)
    get_object(budget_id, db)
    db.query(Budget).filter(Budget.id == budget_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Budget Successfully deleted")
