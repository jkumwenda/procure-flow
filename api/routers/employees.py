from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends,Query
from schemas.schemas import EmployeeSchema
from models import Employee, Users
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(employee_id, db):
    employee = db.query(Employee).filter(Employee.user_id == employee_id).first()
    if employee is None:
        raise HTTPException(
            status_code=404, detail=f"ID {employee_id} : Does not exist"
        )

    return employee


def get_employee_object(employee_id, db):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    employee = employee
    if employee is None:
        employee = False
    return employee


def get_user_object(user_id: int, db: Session):
    query = db.query(Users).filter(Users.id == user_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} does not exist")
    return query


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_employees(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_EMPLOYEE", user["id"], db)
    query = (
        db.query(Employee).filter(Employee.employee_number.ilike(f"%{search}%")).all()
    )

    pages = math.ceil(len(query) / limit)
    data_to_return = query[skip : skip + limit]
    return {"pages": pages, "data": data_to_return}


@router.post("/")
async def add_employee(
    employee_schema: EmployeeSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_EMPLOYEE", user["id"], db)
    employee_model = Employee()

    employee_model.employee_number = employee_schema.employee_number
    db.add(employee_model)
    db.commit()
    return employee_schema


@router.get("/{employee_id}")
async def get_employee(
    employee_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_EMPLOYEE", user["id"], db)

    return get_object(employee_id, db)


@router.get("/user/{id}")
async def get_user_employee(
    id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_EMPLOYEE", user["id"], db)

    employee = db.query(Employee).filter(Employee.user_id == id).first()
    user = employee.user
    branch = employee.branch
    department = employee.department
    position = employee.position
    return {
        "id": employee.id,
        "employee_number": employee.employee_number,
        "user": user,
        "branch": branch,
        "department": department,
        "position": position,
    }


@router.put("/{employee_id}")
async def update_employee(
    employee_id: int,
    employee_schema: EmployeeSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_EMPLOYEE", user["id"], db)
    employee_model = get_employee_object(employee_id, db)

    if not employee_model:
        employee_model = Employee(
            user_id=employee_schema.user_id,
            position_id=employee_schema.position_id,
            branch_id=employee_schema.branch_id,
            department_id=employee_schema.department_id,
            employee_number=employee_schema.employee_number,
        )

    user_model = get_user_object(employee_id, db)
    user_model.firstname = employee_schema.firstname
    user_model.lastname = employee_schema.lastname

    employee_model.user_id = employee_schema.user_id
    employee_model.position_id = employee_schema.position_id
    employee_model.branch_id = employee_schema.branch_id
    employee_model.department_id = employee_schema.department_id
    employee_model.employee_number = employee_schema.employee_number

    db.add(user_model)
    db.add(employee_model)

    db.commit()
    db.refresh(employee_model)

    return employee_schema


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_EMPLOYEE", user["id"], db)
    get_object(employee_id, db)
    db.query(Employee).filter(Employee.id == employee_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Employee Successfully deleted")
