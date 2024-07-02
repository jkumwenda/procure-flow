import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Query
from schemas.schemas import (
    PurchaseOrderSchema,
    PurchaseOrderItemSchema,
    PurchaseOrderApprovalHistorySchema,
)
from models import (
    PurchaseOrder,
    UserDepartment,
    PurchaseOrderItem,
    PurchaseOrderApprovalHistory,
    ApprovalWorkflow,
    UserPosition,
    Users,
    Workflow,
    Position,
    Request,
    PurchaseOrderApprovalHistoryComment,
)
from dependencies import Security
from database import get_db
import math
from datetime import datetime
import utils
import utils
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(purchase_order_id, db):
    purchase_order = (
        db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()
    )
    if purchase_order is None:
        raise HTTPException(
            status_code=404, detail=f"ID {purchase_order_id} : Does not exist"
        )
    return purchase_order


def add_next_approver(next_stage, raiser_id, purchase_order_id, db):
    purchase_order_detail = (
        db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()
    )

    purchase_orderer_detail = (
        db.query(Users).filter(Users.id == purchase_order_detail.raiser_id).first()
    )

    workflow = db.query(Workflow).filter(Workflow.workflow == "LPO").first()
    approval_workflow = (
        db.query(ApprovalWorkflow)
        .filter(
            ApprovalWorkflow.workflow_id == workflow.id,
            ApprovalWorkflow.stage == next_stage,
        )
        .first()
    )

    users_for_position = (
        db.query(Users, Position)
        .join(UserPosition, Users.id == UserPosition.user["id"])
        .join(Position, UserPosition.position_id == Position.id)
        .filter(UserPosition.position_id == approval_workflow.position_id)
        .all()
    )

    purchase_orderer_department = (
        db.query(UserDepartment).filter(UserDepartment.user["id"] == raiser_id).first()
    )

    position_users = []
    for user, position in users_for_position:
        user_department = (
            db.query(UserDepartment)
            .filter(UserDepartment.user["id"] == user.id)
            .first()
        )
        if position.position == "HOD":
            if (
                user_department.department_id
                == purchase_orderer_department.department_id
            ):
                purchase_order_approval_history_model = PurchaseOrderApprovalHistory(
                    purchase_order_id=purchase_order_id,
                    approver_id=int(user.id),
                    approval_status=0,
                    approval_action_id=approval_workflow.approval_action_id,
                    next_stage=int(next_stage),
                )
                db.add(purchase_order_approval_history_model)
                db.commit()
                db.refresh(purchase_order_approval_history_model)
                utils.approve_purchase_order_email(
                    user.email,
                    user.firstname,
                    purchase_orderer_detail,
                    purchase_order_detail,
                )

        elif position.position != "HOD":
            purchase_order_approval_history_model = PurchaseOrderApprovalHistory(
                purchase_order_id=purchase_order_id,
                approver_id=int(user.id),
                approval_status=0,
                approval_action_id=approval_workflow.approval_action_id,
                next_stage=int(next_stage),
            )
            db.add(purchase_order_approval_history_model)
            db.commit()
            db.refresh(purchase_order_approval_history_model)
            utils.approve_purchase_order_email(
                user.email,
                user.firstname,
                purchase_orderer_detail,
                purchase_order_detail,
            )
    return position_users


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_purchase_orders(
    department_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_PURCHASE_ORDER", user["id"], db)

    offset = (skip - 1) * limit
    purchase_orders = (
        db.query(PurchaseOrder)
        .filter(or_(PurchaseOrder.id.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(PurchaseOrder)
        .filter(or_(PurchaseOrder.id.ilike(f"%{search}%")))
        .count()
    )

    if not purchase_orders:
        raise HTTPException(
            status_code=404, detail="No purchase orders found for this purchase_orderor"
        )
    response_data = []

    for purchase_order in purchase_orders:
        department = purchase_order.department
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        purchase_orderer = purchase_order.user
        if not purchase_orderer:
            raise HTTPException(status_code=404, detail="PurchaseOrderer not found")

        response_data.append(
            {
                "purchase_order": {
                    "id": purchase_order.id,
                    "raiser_id": purchase_order.raiser_id,
                    "purchase_order": purchase_order.purchase_order,
                    "purchase_order_date": purchase_order.purchase_order_date,
                    "purchase_order_status": purchase_order.purchase_order_status,
                },
                "department": {
                    "id": department.id,
                    "department": department.department,
                },
                "purchase_orderer": {
                    "id": purchase_orderer.id,
                    "firstname": purchase_orderer.firstname,
                    "lastname": purchase_orderer.lastname,
                    "email": purchase_orderer.email,
                },
            }
        )

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": response_data}


@router.post("/")
async def add_purchase_order(
    purchase_order_schema: PurchaseOrderSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PURCHASE_ORDER", user["id"], db)

    purchase_order = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.request_id == purchase_order_schema.request_id,
            PurchaseOrder.supplier_id == purchase_order_schema.supplier_id,
        )
        .first()
    )

    if purchase_order:
        purchase_order_id = purchase_order.id

    else:
        purchase_order_model = PurchaseOrder(
            request_id=purchase_order_schema.request_id,
            supplier_id=purchase_order_schema.supplier_id,
            raiser_id=user["id"],
            purchase_order_date=datetime.now(),
            purchase_order_status=1,
        )

        db.add(purchase_order_model)
        db.commit()
        db.refresh(purchase_order_model)
        purchase_order_id = purchase_order_model.id

    purchase_order_item_model = PurchaseOrderItem(
        purchase_order_id=purchase_order_id,
        request_item_id=purchase_order_schema.item_id,
        amount=purchase_order_schema.amount,
    )

    db.add(purchase_order_item_model)
    db.commit()
    db.refresh(purchase_order_item_model)

    return {"purchase_order_id": purchase_order_id}


@router.get("/{purchase_order_id}")
async def get_purchase_order(
    purchase_order_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    purchase_order = db.query(PurchaseOrder).get(purchase_order_id)
    if not purchase_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    request = purchase_order.request
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    supplier = purchase_order.supplier
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return {
        "purchase_order": {
            "id": purchase_order.id,
            "request_id": purchase_order.request_id,
            "request": purchase_order.request.request,
            "raiser_id": purchase_order.raiser_id,
            "request_by": purchase_order.request.user.firstname
            + " "
            + purchase_order.request.user.lastname,
            "supplier_id": purchase_order.supplier_id,
            "purchase_order_date": purchase_order.purchase_order_date,
            "purchase_order_status": purchase_order.purchase_order_status,
        },
        "supplier": {
            "id": supplier.id,
            "supplier": supplier.supplier,
            "address": supplier.address,
        },
        "purchase_order_items": [
            {
                "id": purchase_order_item.id,
                "request_item_id": purchase_order_item.request_item.id,
                "item": purchase_order_item.request_item.item.item,
                "purchase_order_id": purchase_order_item.purchase_order_id,
                "description": purchase_order_item.request_item.description,
                "quantity": purchase_order_item.request_item.quantity,
                "amount": purchase_order_item.amount,
            }
            for purchase_order_item in purchase_order.purchase_order_item
        ],
        "purchase_order_approval_history": [
            {
                "id": purchase_order_approval_history.id,
                "approver_id": purchase_order_approval_history.approver_id,
                "firstname": purchase_order_approval_history.user.firstname,
                "lastname": purchase_order_approval_history.user.lastname,
                "approval_status": purchase_order_approval_history.approval_status,
                "date": purchase_order_approval_history.created_at,
                "comment": purchase_order_approval_history.purchase_order_approval_history_comment,
                "approval_action": purchase_order_approval_history.approval_action.approval_action,
            }
            for purchase_order_approval_history in purchase_order.purchase_order_approval_history
        ],
    }


@router.put("/{purchase_order_id}")
async def update_purchase_order(
    purchase_order_id: int,
    purchase_order_schema: PurchaseOrderSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PURCHASE_ORDER", user["id"], db)

    purchase_order_model = get_object(purchase_order_id, db)

    purchase_order_model.request_id = purchase_order_schema.request_id
    purchase_order_model.supplier_id = purchase_order_schema.supplier_id
    db.add(purchase_order_model)
    db.commit()

    return purchase_order_schema


@router.delete("/{purchase_order_id}")
async def delete_purchase_order(
    purchase_order_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PURCHASE_ORDER", user["id"], db)
    get_object(purchase_order_id, db)
    db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Purchase order successfully deleted")


@router.get("/purchase_order/{requester_id}")
async def get_requester_purchase_orders(
    requester_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    if requester_id == 0:
        requester_id = int(user["id"])

    purchase_orders = (
        db.query(PurchaseOrder)
        .join(PurchaseOrder.request)
        .filter(Request.requester_id == requester_id)
        .all()
    )

    if not purchase_orders:
        raise HTTPException(
            status_code=404, detail="No purchase orders found for this requester"
        )
    response_data = []

    for purchase_order in purchase_orders:
        requester = purchase_order.request.user
        if not requester:
            raise HTTPException(status_code=404, detail="Requester not found")

        supplier = purchase_order.supplier
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")

        purchase_order_items_data = [
            {
                "id": purchase_order_item.id,
                "purchase_order_item_id": purchase_order_item.request_item.item_id,
                "item": purchase_order_item.request_item.item.item,
                "amount": purchase_order_item.amount,
            }
            for purchase_order_item in purchase_order.purchase_order_item
        ]

        response_data.append(
            {
                "purchase_order": {
                    "id": purchase_order.id,
                    "requester_id": purchase_order.request.requester_id,
                    "purchase_order": purchase_order.supplier_id,
                    "purchase_order_date": purchase_order.purchase_order_date,
                    "purchase_order_status": purchase_order.purchase_order_status,
                },
                "supplier": {
                    "id": supplier.id,
                    "supplier": supplier.supplier,
                },
                "requester": {
                    "id": requester.id,
                    "firstname": requester.firstname,
                    "lastname": requester.lastname,
                    "email": requester.email,
                },
                "purchase_order_items": purchase_order_items_data,
            }
        )

    return response_data


@router.post("/purchase_order_items/")
async def add_purchase_order_item(
    purchase_order_item_schema: PurchaseOrderItemSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PURCHASE_ORDER", user["id"], db)

    if get_object(purchase_order_item_schema.purchase_order_id, db):
        purchase_order_item_model = PurchaseOrderItem(
            purchase_order_id=purchase_order_item_schema.purchase_order_id,
            request_item_id=purchase_order_item_schema.request_item_id,
            amount=purchase_order_item_schema.amount,
        )

        db.add(purchase_order_item_model)
        db.commit()
        db.refresh(purchase_order_item_model)
        return purchase_order_item_schema


@router.put("/purchase_order_items/{purchase_order_item_id}")
async def update_purchase_order_item(
    purchase_order_item_id: int,
    purchase_order_item_schema: PurchaseOrderItemSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PURCHASE_ORDER", user["id"], db)
    purchase_order_item_model = (
        db.query(PurchaseOrderItem)
        .filter(PurchaseOrderItem.id == purchase_order_item_id)
        .first()
    )

    if purchase_order_item_model:
        purchase_order_item_model.purchase_order_id = (
            purchase_order_item_schema.purchase_order_id
        )
        purchase_order_item_model.request_item_id = (
            purchase_order_item_schema.request_item_id
        )
        purchase_order_item_model.amount = purchase_order_item_schema.amount

        db.add(purchase_order_item_model)
        db.commit()
        db.refresh(purchase_order_item_model)
        return purchase_order_item_schema
    raise HTTPException(status_code=404, detail="Purchase order item was not found")


@router.delete("/purchase_order_items/{purchase_order_item_id}")
async def delete_purchase_order_item(
    purchase_order_item_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PURCHASE_ORDER", user["id"], db)
    db.query(PurchaseOrderItem).filter(
        PurchaseOrderItem.id == purchase_order_item_id
    ).delete()
    db.commit()

    raise HTTPException(
        status_code=200, detail="Purchase order item successfully deleted"
    )


@router.post("/purchase_order_approval_history")
async def add_purchase_order_approval_history(
    purchase_order_approval_history_schema: PurchaseOrderApprovalHistorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PURCHASE_ORDER", user["id"], db)
    purchase_order = get_object(
        purchase_order_approval_history_schema.purchase_order_id, db
    )

    purchase_order_approval_history = (
        db.query(PurchaseOrderApprovalHistory)
        .filter(
            PurchaseOrderApprovalHistory.purchase_order_id
            == purchase_order_approval_history_schema.purchase_order_id
        )
        .first()
    )

    if (purchase_order_approval_history is None) or (
        purchase_order.purchase_order_status == 3
    ):
        # This block will execute only if approval history does not exist
        next_stage = 2
        workflow = db.query(Workflow).filter(Workflow.workflow == "LPO").first()
        approval_workflow = (
            db.query(ApprovalWorkflow)
            .filter(
                ApprovalWorkflow.workflow_id == workflow.id,
                ApprovalWorkflow.stage == next_stage,
            )
            .first()
        )

        approval_action = (
            db.query(ApprovalWorkflow)
            .join(ApprovalWorkflow.position)  # Join the Position relationship
            .filter(Position.position == "Procurement officer")
            .first()
        )

        if approval_workflow is None:
            approval_status = 3
            purchase_order_status = 2
        else:
            approval_status = 1
            purchase_order_status = 1

        if purchase_order.raiser_id != int(user["id"]):
            raise HTTPException(
                status_code=404, detail="Error submitting purchase_order"
            )

        purchase_order_approval_history_model = PurchaseOrderApprovalHistory(
            purchase_order_id=purchase_order_approval_history_schema.purchase_order_id,
            approver_id=int(user["id"]),
            approval_status=approval_status,
            approval_action_id=approval_action.approval_action_id,
            next_stage=int(next_stage),
        )
        db.add(purchase_order_approval_history_model)
        db.commit()
        db.refresh(purchase_order_approval_history_model)

        db.query(PurchaseOrder).filter(
            PurchaseOrder.id == purchase_order_approval_history_schema.purchase_order_id
        ).update({"purchase_order_status": purchase_order_status})

        purchase_order_approval_history_comment_model = PurchaseOrderApprovalHistoryComment(
            purchase_order_approval_history_id=purchase_order_approval_history_model.id,
            comment=purchase_order_approval_history_schema.comment,
        )
        db.add(purchase_order_approval_history_comment_model)
        db.commit()
        db.refresh(purchase_order_approval_history_comment_model)

        if approval_status < 3:
            return add_next_approver(
                next_stage, purchase_order.raiser_id, purchase_order.id, db
            )

    # return purchase_order_approval_history_model
    next_approval = (
        db.query(PurchaseOrderApprovalHistory)
        .filter(
            PurchaseOrderApprovalHistory.purchase_order_id == purchase_order.id,
            PurchaseOrderApprovalHistory.approver_id == int(user["id"]),
            PurchaseOrderApprovalHistory.approval_status == 0,
        )
        .first()
    )
    next_stage = int(next_approval.next_stage) + 1

    workflow = db.query(Workflow).filter(Workflow.workflow == "Procurement").first()

    approval_workflow = (
        db.query(ApprovalWorkflow)
        .filter(
            ApprovalWorkflow.workflow_id == workflow.id,
            ApprovalWorkflow.stage == next_stage,
        )
        .first()
    )

    approval_action = (
        db.query(ApprovalWorkflow)
        .filter(
            ApprovalWorkflow.workflow_id == workflow.id,
            ApprovalWorkflow.stage == next_stage - 1,
        )
        .first()
    )

    if approval_workflow is None:
        approval_status = 3
        purchase_order_status = 4
    else:
        approval_status = 1
        purchase_order_status = 2

    purchase_order_approval_history_model = PurchaseOrderApprovalHistory(
        purchase_order_id=purchase_order_approval_history_schema.purchase_order_id,
        approver_id=int(user["id"]),
        approval_status=approval_status,
        approval_action_id=approval_action.approval_action_id,
        next_stage=int(next_stage),
    )
    db.add(purchase_order_approval_history_model)
    db.commit()
    db.refresh(purchase_order_approval_history_model)

    db.query(PurchaseOrder).filter(
        PurchaseOrder.id == purchase_order_approval_history_schema.purchase_order_id
    ).update({"purchase_order_status": purchase_order_status})

    purchase_order_approval_history_comment_model = PurchaseOrderApprovalHistoryComment(
        purchase_order_approval_history_id=purchase_order_approval_history_model.id,
        comment=purchase_order_approval_history_schema.comment,
    )
    db.add(purchase_order_approval_history_comment_model)
    db.commit()
    db.refresh(purchase_order_approval_history_comment_model)

    db.query(PurchaseOrderApprovalHistory).filter(
        PurchaseOrderApprovalHistory.purchase_order_id == purchase_order.id,
        PurchaseOrderApprovalHistory.approval_status == 0,
    ).update({"approval_status": 4})
    db.commit()

    if approval_status < 3:
        return add_next_approver(
            next_stage, purchase_order.raiser_id, purchase_order.id, db
        )
