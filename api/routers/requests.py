import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Query
from schemas.schemas import (
    RequestSchema,
    RequestItemSchema,
    RequestApprovalHistorySchema,
)
from models import (
    Request,
    UserDepartment,
    RequestItem,
    RequestFile,
    RequestApprovalHistory,
    ApprovalHistoryComment,
    ApprovalWorkflow,
    UserPosition,
    Users,
    Workflow,
    Position,
)
from dependencies import Security
from database import get_db
import math
from datetime import datetime
import uuid
import utils
from dotenv import load_dotenv
from sqlalchemy import or_
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

load_dotenv()

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(request_id, db):
    request = db.query(Request).filter(Request.id == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail=f"ID {request_id} : Does not exist")
    return request


def get_request_file(file_id: int, db: Session):
    file = db.query(RequestFile).filter(RequestFile.id == file_id).first()
    if file is None:
        raise HTTPException(
            status_code=404, detail=f"File with ID {file_id} : does not exist"
        )
    return file


def add_next_approver(next_stage, requester_id, request_id, db):
    request_detail = db.query(Request).filter(Request.id == request_id).first()

    requester_detail = (
        db.query(Users).filter(Users.id == request_detail.requester_id).first()
    )

    workflow = db.query(Workflow).filter(Workflow.workflow == "Procurement").first()
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
        .join(UserPosition, Users.id == UserPosition.user_id)
        .join(Position, UserPosition.position_id == Position.id)
        .filter(UserPosition.position_id == approval_workflow.position_id)
        .all()
    )

    requester_department = (
        db.query(UserDepartment).filter(UserDepartment.user_id == requester_id).first()
    )

    position_users = []
    for user, position in users_for_position:
        user_department = (
            db.query(UserDepartment).filter(UserDepartment.user_id == user.id).first()
        )
        if position.position == "HOD":
            if user_department.department_id == requester_department.department_id:
                request_approval_history_model = RequestApprovalHistory(
                    request_id=request_id,
                    approver_id=int(user.id),
                    approval_status=0,
                    approval_action_id=approval_workflow.approval_action_id,
                    next_stage=int(next_stage),
                )
                db.add(request_approval_history_model)
                db.commit()
                db.refresh(request_approval_history_model)
                utils.approve_request_email(
                    user.email, user.firstname, requester_detail, request_detail
                )

        elif position.position != "HOD":
            request_approval_history_model = RequestApprovalHistory(
                request_id=request_id,
                approver_id=int(user.id),
                approval_status=0,
                approval_action_id=approval_workflow.approval_action_id,
                next_stage=int(next_stage),
            )
            db.add(request_approval_history_model)
            db.commit()
            db.refresh(request_approval_history_model)
            utils.approve_request_email(
                user.email, user.firstname, requester_detail, request_detail
            )
    return position_users


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_requests(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_REQUEST", user["id"], db)

    offset = (skip - 1) * limit
    requests = (
        db.query(Request)
        .filter(or_(Request.request.ilike(f"%{search}%")))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Request).filter(or_(Request.request.ilike(f"%{search}%"))).count()
    )

    if not requests:
        raise HTTPException(
            status_code=404, detail="No requests found for this requestor"
        )
    response_data = []

    for request in requests:
        department = request.department
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        requester = request.user
        if not requester:
            raise HTTPException(status_code=404, detail="Requester not found")

        response_data.append(
            {
                "request": {
                    "id": request.id,
                    "requester_id": request.requester_id,
                    "request": request.request,
                    "request_date": request.request_date,
                    "request_status": request.request_status,
                },
                "department": {
                    "id": department.id,
                    "department": department.department,
                },
                "requester": {
                    "id": requester.id,
                    "firstname": requester.firstname,
                    "lastname": requester.lastname,
                    "email": requester.email,
                },
            }
        )

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": response_data}


@router.post("/")
async def add_request(
    request_schema: RequestSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_REQUEST", user["id"], db)

    user_department = (
        db.query(UserDepartment).filter(UserDepartment.user_id == user["id"]).first()
    )
    user_id = user["id"]
    if not user_department:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} does not have a department",
        )
    department_id = user_department.department_id
    request_model = Request(
        request=request_schema.request,
        requester_id=user["id"],
        department_id=department_id,
        request_date=datetime.now(),
        request_status=1,
    )
    db.add(request_model)
    db.commit()
    db.refresh(request_model)
    return {"request_id": request_model.id}


@router.get("/{request_id}")
async def get_request(
    request_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_REQUEST", user["id"], db)
    request = db.query(Request).get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    department = request.department
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    requester = request.user
    if not requester:
        raise HTTPException(status_code=404, detail="Requester not found")

    return {
        "request": {
            "id": request.id,
            "requester_id": request.requester_id,
            "request": request.request,
            "request_date": request.request_date,
            "request_status": request.request_status,
        },
        "department": {
            "id": department.id,
            "department": department.department,
        },
        "requester": {
            "id": requester.id,
            "firstname": requester.firstname,
            "lastname": requester.lastname,
            "email": requester.email,
        },
        "items": [
            {
                "id": item.id,
                "item_id": item.item.id,
                "item": item.item.item,
                "unit_of_measure": item.item.unit_of_measure.unit_of_measure,
                "description": item.description,
                "quantity": item.quantity,
            }
            for item in request.request_item
        ],
        "purchase_orders": [
            {
                "id": purchase_order.id,
                "purchase_oder_id": purchase_order.id,
                "request_id": purchase_order.request_id,
                "supplier_id": purchase_order.supplier_id,
                "supplier": purchase_order.supplier.supplier,
            }
            for purchase_order in request.purchase_order
        ],
        "api_url": os.getenv("BASE_URL"),
        "files": [
            {
                "id": file.id,
                "file_name": file.file_name,
                "real_file_name": file.real_file_name,
                "file_type": file.file_type,
                "file_location": file.file_location,
            }
            for file in request.request_file
        ],
        "request_approval_history": [
            {
                "id": request_approval_history.id,
                "approver_id": request_approval_history.approver_id,
                "firstname": request_approval_history.user.firstname,
                "lastname": request_approval_history.user.lastname,
                "approval_status": request_approval_history.approval_status,
                "date": request_approval_history.created_at,
                "comment": request_approval_history.approval_history_comment,
                "approval_action": request_approval_history.approval_action.approval_action,
            }
            for request_approval_history in request.request_approval_history
        ],
    }


@router.put("/{request_id}")
async def update_request(
    request_id: int,
    request_schema: RequestSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_REQUEST", user["id"], db)
    request_model = get_object(request_id, db)

    request_model.request = (request_schema.request,)
    db.add(request_model)
    db.commit()

    return request_schema


@router.delete("/{request_id}")
async def delete_request(
    request_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_REQUEST", user["id"], db)
    get_object(request_id, db)
    db.query(Request).filter(Request.id == request_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Request Successfully deleted")


@router.get("/requester/{requester_id}")
async def get_my_requests(
    requester_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    if requester_id == 0:
        requester_id = int(user["id"])

    requests = db.query(Request).filter(Request.requester_id == requester_id).all()

    if not requests:
        raise HTTPException(
            status_code=404, detail="No requests found for this requestor"
        )
    response_data = []

    for request in requests:
        department = request.department
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        requester = request.user
        if not requester:
            raise HTTPException(status_code=404, detail="Requester not found")

        items_data = [
            {
                "id": item.id,
                "item_id": item.item.id,
                "description": item.description,
                "quantity": item.quantity,
                "item_name": item.item.item,
                "unit_of_measure": item.item.unit_of_measure.unit_of_measure,
            }
            for item in request.request_item
        ]

        response_data.append(
            {
                "request": {
                    "id": request.id,
                    "requester_id": request.requester_id,
                    "request": request.request,
                    "request_date": request.request_date,
                    "request_status": request.request_status,
                },
                "department": {
                    "id": department.id,
                    "department": department.department,
                },
                "requester": {
                    "id": requester.id,
                    "firstname": requester.firstname,
                    "lastname": requester.lastname,
                    "email": requester.email,
                },
                "items": items_data,
            }
        )
    return response_data


@router.post("/request_items/")
async def add_request_item(
    request_item_schema: RequestItemSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_REQUEST", user["id"], db)

    if get_object(request_item_schema.request_id, db):
        request_item_model = RequestItem(
            request_id=request_item_schema.request_id,
            item_id=request_item_schema.item_id,
            description=request_item_schema.description,
            quantity=request_item_schema.quantity,
        )
        db.add(request_item_model)
        db.commit()
        db.refresh(request_item_model)
        return request_item_schema


@router.put("/request_items/{request_item_id}")
async def update_request_item(
    request_item_id: int,
    request_item_schema: RequestItemSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_REQUEST", user["id"], db)
    request_item_model = (
        db.query(RequestItem).filter(RequestItem.id == request_item_id).first()
    )

    if request_item_model:
        request_item_model.item_id = request_item_schema.item_id
        request_item_model.description = request_item_schema.description
        request_item_model.quantity = request_item_schema.quantity

        db.add(request_item_model)
        db.commit()
        db.refresh(request_item_model)
        return request_item_schema
    raise HTTPException(status_code=404, detail="Request item was not found")


@router.delete("/request_items/{request_item_id}")
async def delete_request_item(
    request_item_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_REQUEST", user["id"], db)
    db.query(RequestItem).filter(RequestItem.id == request_item_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Request item successfully deleted")


@router.post("/request_files/")
async def upload_file(
    user: user_dependency,
    file: UploadFile = File(...),
    request_id: int = Form(...),
    file_name: str = Form(...),
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_REQUEST", user["id"], db)

    file_location = uuid.uuid4().hex
    os.mkdir(f"uploads/{file_location}")

    try:
        with open(f"uploads/{file_location}/{file.filename}", "wb") as f:
            f.write(file.file.read())
            request_file_model = RequestFile(
                file_name=file_name,
                real_file_name=file.filename,
                request_id=request_id,
                file_size=0,
                file_type=file.content_type,
                file_location=(f"uploads/{file_location}/{file.filename}"),
            )

            db.add(request_file_model)
            db.commit()
            db.refresh(request_file_model)

            if request_file_model.id is not None:
                return {
                    "request_file_id": request_file_model.id,
                    "file_name": file.filename,
                    "real_file_name": file.filename,
                    "request_id": request_id,
                    "file_type": file.content_type,
                    "file_location": (f"uploads/{file_location}"),
                }
        os.remove(file_location)
        raise HTTPException(
            status_code=404, detail="File creation in database failed, file deleted"
        )
    except Exception as e:
        return {"error": str(e)}


@router.get("/download_request_file/{file_id}")
async def download_request_file(
    file_id: int,
    db: Session = Depends(get_db),
    # user["id"]: str = Depends(oauth2.require_user),
):
    # security.secureAccess("VIEW_REQUEST", user["id"], db)
    file = get_request_file(file_id, db)

    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = file.file_location
    utils.validate_file_path(file_path)

    filename = str(file.real_file_name)
    return utils.download_file(file_path, filename)


@router.post("/request_approval_history/")
async def add_request_approval_history(
    request_approval_history_schema: RequestApprovalHistorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_REQUEST", user["id"], db)

    request = get_object(request_approval_history_schema.request_id, db)

    request_approval_history = (
        db.query(RequestApprovalHistory)
        .filter(
            RequestApprovalHistory.request_id
            == request_approval_history_schema.request_id
        )
        .first()
    )

    if (request_approval_history is None) or (request.request_status == 3):
        next_stage = 2
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
            .join(ApprovalWorkflow.position)  # Join the Position relationship
            .filter(Position.position == "All staff")
            .first()
        )

        if approval_workflow is None:
            approval_status = 3
            request_status = 4
        else:
            approval_status = 1
            request_status = 2

        if request.requester_id != int(user["id"]):
            raise HTTPException(status_code=404, detail="Error submitting request")

        request_approval_history_model = RequestApprovalHistory(
            request_id=request_approval_history_schema.request_id,
            approver_id=int(user["id"]),
            approval_status=approval_status,
            approval_action_id=approval_action.approval_action_id,
            next_stage=int(next_stage),
        )
        db.add(request_approval_history_model)
        db.commit()
        db.refresh(request_approval_history_model)

        db.query(Request).filter(
            Request.id == request_approval_history_schema.request_id
        ).update({"request_status": request_status})

        approval_history_comment_model = ApprovalHistoryComment(
            request_approval_history_id=request_approval_history_model.id,
            comment=request_approval_history_schema.comment,
        )
        db.add(approval_history_comment_model)
        db.commit()
        db.refresh(approval_history_comment_model)

        if approval_status < 3:
            return add_next_approver(next_stage, request.requester_id, request.id, db)

    # return request_approval_history_model
    next_approval = (
        db.query(RequestApprovalHistory)
        .filter(
            RequestApprovalHistory.request_id == request.id,
            RequestApprovalHistory.approver_id == int(user["id"]),
            RequestApprovalHistory.approval_status == 0,
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
        request_status = 4
    else:
        approval_status = 1
        request_status = 2

    request_approval_history_model = RequestApprovalHistory(
        request_id=request_approval_history_schema.request_id,
        approver_id=int(user["id"]),
        approval_status=approval_status,
        approval_action_id=approval_action.approval_action_id,
        next_stage=int(next_stage),
    )
    db.add(request_approval_history_model)
    db.commit()
    db.refresh(request_approval_history_model)

    db.query(Request).filter(
        Request.id == request_approval_history_schema.request_id
    ).update({"request_status": request_status})

    approval_history_comment_model = ApprovalHistoryComment(
        request_approval_history_id=request_approval_history_model.id,
        comment=request_approval_history_schema.comment,
    )
    db.add(approval_history_comment_model)
    db.commit()
    db.refresh(approval_history_comment_model)

    db.query(RequestApprovalHistory).filter(
        RequestApprovalHistory.request_id == request.id,
        RequestApprovalHistory.approval_status == 0,
    ).update({"approval_status": 4})
    db.commit()

    if approval_status < 3:
        return add_next_approver(next_stage, request.requester_id, request.id, db)


@router.post("/request_reject_history/")
async def add_request_reject_approval_history(
    request_approval_history_schema: RequestApprovalHistorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_REQUEST", user["id"], db)
    request = get_object(request_approval_history_schema.request_id, db)
    user = db.query(Users).filter(Users.id == request.requester_id).first()
    approval_workflow = (
        db.query(ApprovalWorkflow)
        .join(ApprovalWorkflow.position)  # Join the Position relationship
        .filter(Position.position == "All staff")
        .first()
    )

    db.query(RequestApprovalHistory).filter(
        Request.id == request_approval_history_schema.request_id,
        RequestApprovalHistory.approval_status == 0,
    ).update({"approval_status": 1})

    request_approval_history_model = RequestApprovalHistory(
        request_id=request_approval_history_schema.request_id,
        approver_id=user.id,
        approval_status=2,
        approval_action_id=approval_workflow.approval_action_id,
        next_stage=1,
    )
    db.add(request_approval_history_model)
    db.commit()
    db.refresh(request_approval_history_model)

    db.query(Request).filter(
        Request.id == request_approval_history_schema.request_id
    ).update({"request_status": 3})

    approval_history_comment_model = ApprovalHistoryComment(
        request_approval_history_id=request_approval_history_model.id,
        comment=request_approval_history_schema.comment,
    )
    db.add(approval_history_comment_model)
    db.commit()
    db.refresh(approval_history_comment_model)

    utils.reject_request_email(user.email, user.firstname, request)

    raise HTTPException(status_code=200, detail="Request reject successfully")


@router.get("/notifications/", response_model=dict)
async def get_notifications(
    user: user_dependency,
    db: Session = Depends(get_db),
):
    # Query for request approval history
    request_approval_history = (
        db.query(RequestApprovalHistory)
        .filter(
            RequestApprovalHistory.approver_id == user["id"],
            RequestApprovalHistory.approval_status == 0,
        )
        .all()
    )

    # Calculate total approvals
    total_approvals = len(request_approval_history)

    # Check if there are any notifications
    if not request_approval_history:
        raise HTTPException(
            status_code=404, detail="No request history found for this user's attention"
        )

    # Prepare the response data
    notifications = []
    for request_history in request_approval_history:
        request = request_history.request
        requester = request_history.user

        # Check for missing data
        if not request or not requester:
            raise HTTPException(
                status_code=404, detail="Missing request or requester data"
            )

        notifications.append(
            {
                "id": request_history.id,
                "approval_status": request_history.approval_status,
                "request_id": request.id,
                "request": request.request,
                "date": request.request_date,
                "firstname": requester.firstname,
                "lastname": requester.lastname,
            }
        )

    # Construct the response dictionary
    response_data = {"notifications": notifications, "total_approvals": total_approvals}
    return response_data
