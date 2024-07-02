from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import PermissionSchema
from models import Permission
from dependencies import Security
from database import get_db
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(permission_id, db):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if permission is None:
        raise HTTPException(
            status_code=404, detail=f"ID {permission_id} : Does not exist"
        )

    return permission


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_permissions(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("READ_PERMISSION", user["id"], db)
    query = (
        db.query(Permission)
        .filter(
            or_(
                Permission.permission.ilike(f"%{search}%"),
                Permission.permission_code.ilike(f"%{search}%"),
            )
        )
        .all()
    )
    return {"data": query}


@router.post("/")
async def create_permission(
    permission_schema: PermissionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("WRITE_PERMISSION", user["id"], db)
    permission_model = Permission()
    permission_model.permission = permission_schema.permission
    permission_model.permission_code = permission_schema.permission_code
    db.add(permission_model)
    db.commit()
    return permission_schema


@router.put("/{permission_id}")
async def update_permission(
    permission_id: int,
    permission_schema: PermissionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PERMISSION", user["id"], db)
    permission_model = get_object(permission_id, db)

    permission_model.permission = permission_schema.permission
    permission_model.permission_code = permission_schema.permission_code
    db.commit()

    return permission_schema


@router.get("/{permission_id}")
async def get_permission(
    permission_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("READ_PERMISSION", user["id"], db)
    return get_object(permission_id, db)


@router.delete("/{permission_id}")
async def delete_permission(
    permission_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PERMISSION", user["id"], db)
    get_object(permission_id, db)

    db.query(Permission).filter(Permission.id == permission_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Permission Successfully deleted")
