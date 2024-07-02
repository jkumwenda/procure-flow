from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import WorkflowSchema, ApprovalWorkflowSchema
from models import Workflow, ApprovalWorkflow
from dependencies import Security
from database import get_db
import math
from itertools import groupby
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(workflow_id, db):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(
            status_code=404, detail=f"ID {workflow_id} : Does not exist"
        )
    return workflow


def get_approval_object(approval_workflow_id, db):
    approval_workflow = (
        db.query(ApprovalWorkflow)
        .filter(ApprovalWorkflow.id == approval_workflow_id)
        .first()
    )
    if approval_workflow is None:
        raise HTTPException(
            status_code=404, detail=f"ID {approval_workflow_id} : Does not exist"
        )
    return approval_workflow


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_workflows(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_WORKFLOW", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(Workflow)
        .filter(or_(Workflow.workflow.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Workflow).filter(or_(Workflow.workflow.ilike(f"%{search}%"))).count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_workflow(
    workflow_schema: WorkflowSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_WORKFLOW", user["id"], db)
    approval_workflow_model = Workflow()

    approval_workflow_model.workflow = workflow_schema.workflow
    approval_workflow_model.description = workflow_schema.description
    db.add(approval_workflow_model)
    db.commit()
    return workflow_schema


@router.get("/{workflow_id}")
async def get_workflow(
    workflow_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_WORKFLOW", user["id"], db)
    workflow = get_object(workflow_id, db)
    return {
        "workflow": {
            "id": workflow.id,
            "workflow": workflow.workflow,
            "description": workflow.description,
        },
        "approval_workflows": [
            {
                "id": approval_work_flow.id,
                "position_id": approval_work_flow.position_id,
                "position": approval_work_flow.position.position,
                "department_id": approval_work_flow.department_id,
                "department": approval_work_flow.department.department,
                "approval_action_id": approval_work_flow.approval_action_id,
                "approval_action": approval_work_flow.approval_action.approval_action,
                "stage": approval_work_flow.stage,
                "order": approval_work_flow.order,
            }
            for approval_work_flow in workflow.approval_workflow
        ],
    }


@router.put("/{workflow_id}")
async def update_workflow(
    workflow_id: int,
    workflow_schema: WorkflowSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_WORKFLOW", user["id"], db)
    approval_workflow_model = get_object(workflow_id, db)

    approval_workflow_model.workflow = workflow_schema.workflow
    approval_workflow_model.description = workflow_schema.description
    db.add(approval_workflow_model)
    db.commit()

    return workflow_schema


@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_WORKFLOW", user["id"], db)
    get_object(workflow_id, db)
    db.query(Workflow).filter(Workflow.id == workflow_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Workflow Successfully deleted")


@router.post("/approval_workflows/")
async def add_approval_workflow(
    approval_workflow_schema: ApprovalWorkflowSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_WORKFLOW", user["id"], db)

    approval_workflow_model = ApprovalWorkflow(
        workflow_id=approval_workflow_schema.workflow_id,
        position_id=approval_workflow_schema.position_id,
        department_id=approval_workflow_schema.department_id,
        approval_action_id=approval_workflow_schema.approval_action_id,
        stage=approval_workflow_schema.stage,
        order=approval_workflow_schema.order,
    )

    db.add(approval_workflow_model)
    db.commit()
    db.refresh(approval_workflow_model)
    return approval_workflow_model


@router.put("/approval_workflows/{approval_workflow_id}")
async def update_approval_workflow(
    approval_workflow_id: int,
    approval_workflow_schema: ApprovalWorkflowSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_WORKFLOW", user["id"], db)
    approval_workflow_model = get_approval_object(approval_workflow_id, db)

    approval_workflow_model.workflow_id = (approval_workflow_schema.workflow_id,)
    approval_workflow_model.position_id = (approval_workflow_schema.position_id,)
    approval_workflow_model.department_id = (approval_workflow_schema.department_id,)
    approval_workflow_model.approval_action_id = (
        approval_workflow_schema.approval_action_id,
    )
    approval_workflow_model.stage = (approval_workflow_schema.stage,)
    approval_workflow_model.order = (approval_workflow_schema.order,)

    db.add(approval_workflow_model)
    db.commit()
    db.refresh(approval_workflow_model)
    return approval_workflow_model


@router.delete("/approval_workflows/{approval_workflow_id}")
async def delete_approval_workflow(
    approval_workflow_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_WORKFLOW", user["id"], db)
    get_approval_object(approval_workflow_id, db)
    db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.id == approval_workflow_id
    ).delete()
    db.commit()

    raise HTTPException(
        status_code=200, detail="Approval Workflow Successfully deleted"
    )
