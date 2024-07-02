from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import DepartmentSchema
from models import Department
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(department_id, db):
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(
            status_code=404, detail=f"ID {department_id} : Does not exist"
        )
    return department


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_departments(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_BRANCH", user["id"], db)

    query = (
        db.query(Department).filter(Department.department.ilike(f"%{search}%")).all()
    )

    offset = (skip - 1) * limit
    query = (
        db.query(Department)
        .filter(or_(Department.department.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Department)
        .filter(or_(Department.department.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_department(
    department_schema: DepartmentSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_BRANCH", user["id"], db)
    department_model = Department()

    department_model.department = department_schema.department
    db.add(department_model)
    db.commit()
    return department_schema


@router.get("/{department_id}")
async def get_department(
    department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_BRANCH", user["id"], db)
    return get_object(department_id, db)


@router.put("/{department_id}")
async def update_department(
    department_id: int,
    department_schema: DepartmentSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_BRANCH", user["id"], db)
    department_model = get_object(department_id, db)

    department_model.department = department_schema.department
    db.add(department_model)
    db.commit()

    return department_schema


@router.delete("/{department_id}")
async def delete_department(
    department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BRANCH", user["id"], db)
    get_object(department_id, db)
    db.query(Department).filter(Department.id == department_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Department Successfully deleted")