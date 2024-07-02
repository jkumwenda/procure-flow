from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models import Users, Request, Budget
from dependencies import Security
from database import get_db
from sqlalchemy import func
from dependencies import Security
from .auth import get_current_user
from typing import Annotated

security = Security()
user_dependency = Annotated[dict, Depends(get_current_user)]

security = Security()

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_dashboard_data(
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_DASHBOARD", user["id"], db)
    requester_id = int(user["id"])

    user = db.query(Users).filter(Users.id == user["id"]).first()
    user_total_requests = len(user.request)
    approved_requests = len(
        [request for request in user.request if request.request_status == 3]
    )
    total_requests = len(db.query(Request).all())

    total_amount = db.query(func.sum(Budget.amount)).scalar()
    if total_amount is None:
        total_amount = 0

    limited_requests = user.request[:4]
    return {
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "user_total_requests": user_total_requests,
            "approved_requests": approved_requests,
        },
        "positions": [
            {
                "id": position.position.id,
                "position": position.position.position,
            }
            for position in user.user_position
        ],
        "requests": [
            {
                "id": request.id,
                "request": request.request,
                "date": request.request_date,
            }
            for request in limited_requests
        ],
        "total_requests": total_requests,
        "total_budget": total_amount,
    }
