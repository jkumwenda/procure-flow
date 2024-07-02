import os
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Query
from models import DepartmentFile, Department, FileCategory
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
import uuid
import utils
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(department_record_id, db):
    department_record = (
        db.query(DepartmentFile)
        .filter(DepartmentFile.id == department_record_id)
        .first()
    )
    if department_record is None:
        raise HTTPException(
            status_code=404, detail=f"ID {department_record_id} : Does not exist"
        )
    return department_record


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/department_files/{department_id}")
async def get_department_records(
    department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_BRANCH", user["id"], db)
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    offset = (skip - 1) * limit

    query = (
        db.query(DepartmentFile)
        .filter(DepartmentFile.department_id == department_id)
        .join(FileCategory, DepartmentFile.file_category_id == FileCategory.id)
        .filter(
            or_(
                DepartmentFile.file_name.ilike(f"%{search}%"),
                DepartmentFile.real_file_name.ilike(f"%{search}%"),
                FileCategory.file_category.ilike(f"%{search}%"),
            )
        )
        .options(joinedload(DepartmentFile.file_category))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_count = (
        db.query(DepartmentFile)
        .join(FileCategory, DepartmentFile.file_category_id == FileCategory.id)
        .filter(
            or_(
                DepartmentFile.file_name.ilike(f"%{search}%"),
                DepartmentFile.real_file_name.ilike(f"%{search}%"),
                FileCategory.file_category.ilike(f"%{search}%"),
            )
        )
        .filter(DepartmentFile.department_id == department_id)
        .count()
    )

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "department": department, "data": query}


@router.post("/upload_department_file/")
async def add_department_record(
    user: user_dependency,
    file: UploadFile = File(...),
    file_category_id=File(...),
    department_id: int = Form(...),
    file_name: str = Form(...),
    access_level: str = Form(...),
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_REQUEST", user["id"], db)

    file_location = uuid.uuid4().hex
    os.mkdir(f"uploads/{file_location}")

    try:
        with open(f"uploads/{file_location}/{file.filename}", "wb") as f:
            f.write(file.file.read())
            department_file_model = DepartmentFile(
                file_name=file_name,
                real_file_name=file.filename,
                file_category_id=file_category_id,
                department_id=department_id,
                access_level=access_level,
                file_size=0,
                file_type=file.content_type,
                file_location=(f"uploads/{file_location}/{file.filename}"),
            )

            db.add(department_file_model)
            db.commit()
            db.refresh(department_file_model)

            if department_file_model.id is not None:
                return {
                    "id": department_file_model.id,
                    "file_name": file.filename,
                    "real_file_name": file.filename,
                    "file_category_id": file_category_id,
                    "department_id": department_id,
                    "access_level": access_level,
                    "file_type": file.content_type,
                    "file_location": (f"uploads/{file_location}"),
                }
        os.remove(file_location)
        raise HTTPException(
            status_code=404, detail="File creation in database failed, file deleted"
        )
    except Exception as e:
        return {"error": str(e)}


@router.get("/download_file")
async def download_file(
    file_location: str,
    file_name: str,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_REQUEST", user["id"], db)
    file_path = file_location
    utils.validate_file_path(file_path)

    filename = str(file_name)
    return utils.download_file(file_path, filename)


@router.delete("/delete_department_file/{department_file_id}")
async def delete_department_file(
    department_file_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    # security.secureAccess("DELETE_DEPARTMENT_FILE", user["id"], db)
    department_file = (
        db.query(DepartmentFile).filter(DepartmentFile.id == department_file_id).first()
    )
    os.remove(department_file.file_location)
    db.query(DepartmentFile).filter(DepartmentFile.id == department_file_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail=f"Department file Successfully deleted")
