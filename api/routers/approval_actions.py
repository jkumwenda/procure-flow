from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import ApprovalActionSchema
from models import ApprovalAction
from dependencies import Security
from database import get_db
import math
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(approval_action_id, db):
    approval_action = (
        db.query(ApprovalAction).filter(ApprovalAction.id == approval_action_id).first()
    )
    if approval_action is None:
        raise HTTPException(
            status_code=404, detail=f"ID {approval_action_id} : Does not exist"
        )
    return approval_action


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_approval_actions(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_APPROVAL_ACTION", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(ApprovalAction)
        .filter(or_(ApprovalAction.approval_action.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(ApprovalAction)
        .filter(or_(ApprovalAction.approval_action.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_approval_action(
    approval_action_schema: ApprovalActionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_APPROVAL_ACTION", user["id"], db)

    approval_action_model = ApprovalAction(
        approval_action=approval_action_schema.approval_action,
        description=approval_action_schema.description,
    )

    db.add(approval_action_model)
    db.commit()

    return approval_action_schema


@router.get("/{approval_action_id}")
async def get_approval_action(
    approval_action_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_APPROVAL_ACTION", user["id"], db)
    return get_object(approval_action_id, db)


@router.put("/{approval_action_id}")
async def update_approval_action(
    approval_action_id: int,
    approval_action_schema: ApprovalActionSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_APPROVAL_ACTION", user["id"], db)
    approval_action_model = get_object(approval_action_id, db)

    approval_action_model.approval_action = approval_action_schema.approval_action
    approval_action_model.description = approval_action_schema.description
    db.add(approval_action_model)
    db.commit()

    return approval_action_schema


@router.delete("/{approval_action_id}")
async def delete_approval_action(
    approval_action_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_APPROVAL_ACTION", user["id"], db)
    get_object(approval_action_id, db)
    db.query(ApprovalAction).filter(ApprovalAction.id == approval_action_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Unit of measure successfully deleted")
