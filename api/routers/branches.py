from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import BranchSchema, BranchDepartmentSchema
from models import Branch, BranchDepartment
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(branch_id, db):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail=f"ID {branch_id} : Does not exist")

    return branch


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_branches(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_BRANCH", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(Branch)
        .filter(or_(Branch.branch.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Branch).filter(or_(Branch.branch.ilike(f"%{search}%"))).count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_branch(
    branch_schema: BranchSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_BRANCH", user["id"], db)
    branch_model = Branch()

    branch_model.branch = branch_schema.branch
    db.add(branch_model)
    db.commit()
    return branch_schema


@router.get("/{branch_id}")
async def get_branch(
    branch_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_BRANCH", user["id"], db)
    return get_object(branch_id, db)


@router.put("/{branch_id}")
async def update_branch(
    branch_id: int,
    branch_schema: BranchSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_BRANCH", user["id"], db)
    branch_model = get_object(branch_id, db)

    branch_model.branch = branch_schema.branch
    db.add(branch_model)
    db.commit()

    return branch_schema


@router.delete("/{branch_id}")
async def delete_branch(
    branch_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BRANCH", user["id"], db)
    get_object(branch_id, db)
    db.query(Branch).filter(Branch.id == branch_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Branch Successfully deleted")


@router.get("/departments/")
async def get_branch_departments(
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_BRANCH", user["id"], db)
    # Fetch branches with their associated departments
    branches = db.query(Branch).all()
    branches_with_departments = []

    for branch in branches:
        branch_data = {
            "branch_id": branch.id,
            "branch": branch.branch,
            "departments": [
                {"department_id": dep.id, "department": dep.department}
                for dep in branch.departments
            ],
        }
        branches_with_departments.append(branch_data)
    return branches_with_departments


@router.post("/departments/")
async def add_branch_department(
    branch_department_schema: BranchDepartmentSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_BRANCH", user["id"], db)
    branch_department_model = BranchDepartment()
    branch_department_model.department_id = branch_department_schema.department_id
    branch_department_model.branch_id = branch_department_schema.branch_id
    db.add(branch_department_model)
    db.commit()
    return branch_department_schema


@router.get("/departments/{branch_id}")
async def get_branch_departments(
    branch_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_BRANCH", user["id"], db)
    branch = get_object(branch_id, db)
    departments = branch.departments
    return {"branch": branch.branch, "departments": departments}


@router.post("/remove_department/")
async def remove_department_from_branch(
    branch_department_schema: BranchDepartmentSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_BRANCH", user["id"], db)

    db.query(BranchDepartment).filter(
        BranchDepartment.branch_id == branch_department_schema.branch_id,
        BranchDepartment.department_id == branch_department_schema.department_id,
    ).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Branch Successfully deleted")
