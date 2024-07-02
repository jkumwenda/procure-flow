from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime, date


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str
    password: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Black",
                "email": "jonblack@email.com",
                "phone": "0999371088",
                "password": "password",
            }
        }


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserBaseSchema(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Black",
                "email": "jonblack@email.com",
                "phone": "0999371088",
            }
        }


class RoleSchema(BaseModel):
    role: str = Field(min_length=2)
    description: str = Field(min_length=2)

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {"role": "Superuser", "description": "Main system user"}
        }


class PermissionSchema(BaseModel):
    permission: str = Field(min_length=2)
    permission_code: str = Field(min_length=2)

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "permission": "Create system user",
                "permission_code": "create_user",
            }
        }


class RolePermissionSchema(BaseModel):
    role_id: int
    permission_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "role_id": 1,
                "permission_id": 1,
            }
        }


class UserRoleSchema(BaseModel):
    user_id: int
    role_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "role_id": 1,
            }
        }


class FileCategorySchema(BaseModel):
    file_category: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "file_category": "Budget File(s)",
            }
        }


class BusinessCategorySchema(BaseModel):
    business_category: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "business_category": "Retail",
            }
        }


class PersonnelCadreSchema(BaseModel):
    personnel_cadre: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "personnel_cadre": "Pharmacist",
            }
        }


class PositionSchema(BaseModel):
    position: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "position": "Director General",
            }
        }


class UserPositionSchema(BaseModel):
    user_id: int
    position_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "position_id": 1,
            }
        }


class ModuleSchema(BaseModel):
    module: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "module": "Personnel",
            }
        }


class BranchSchema(BaseModel):
    branch: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "branch": "Lilongwe (HQ))",
            }
        }


class DepartmentSchema(BaseModel):
    department: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "department": "Finance",
            }
        }


class UserDepartmentSchema(BaseModel):
    user_id: int
    department_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "department_id": 1,
            }
        }


class BranchDepartmentSchema(BaseModel):
    branch_id: int
    department_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "branch_id": 1,
                "department_id": 1,
            }
        }


class EmployeeSchema(BaseModel):
    firstname: str
    lastname: str
    email: str
    phone: str
    user_id: int
    position_id: int
    branch_id: int
    department_id: int
    employee_number: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "firstname": "Joel",
                "lastname": "Kumwenda",
                "email": "jkumwenda@gmail.com",
                "phone": "+265999371088",
                "user_id": 1,
                "position_id": 1,
                "employee_number": "PMRA 001234",
                "branch_id": 1,
                "department_id": 1,
            }
        }


# Workflow schemas
class RequestSchema(BaseModel):
    request: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "request": "Request title",
            }
        }


class RequestItemSchema(BaseModel):
    request_id: int
    item_id: int
    description: str
    quantity: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "request_id": 1,
                "item_id": 1,
                "description": "Item description",
                "quantity": 2,
            }
        }


class RequesItemtSchema(BaseModel):
    requester_id: int
    item_id: int
    quantity: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {"requester_id": 1, "item_id": 1, "quantity": 5}
        }


class ApprovalActionSchema(BaseModel):
    approval_action: str
    description: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "approval_action": "each",
                "description": "Allow user to add submit request",
            }
        }


class SupplierSchema(BaseModel):
    supplier: str
    address: str
    email: str
    phone: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "supplier": "Pure ICT",
                "address": "Lilongwe City Center, Yabana Buidling",
                "email": "supplier@email.com",
                "phone": "0999371088",
            }
        }


class SupplierCategorySchema(BaseModel):
    supplier_category: str
    description: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "supplier_category": "Statinery",
                "description": "Stationery",
            }
        }


class SupplierSupplierCategorySchema(BaseModel):
    supplier_id: int
    supplier_category_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "supplier_id": 1,
                "supplier_category_id": 1,
            }
        }


class WorkflowSchema(BaseModel):
    workflow: str
    description: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {"workflow": "Procurement", "description": "Description here"}
        }


class ApprovalWorkflowSchema(BaseModel):
    workflow_id: int
    position_id: int
    department_id: int
    approval_action_id: int
    stage: int
    order: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "workflow_id": 1,
                "position_id": 1,
                "department_id": 1,
                "approval_action_id": 1,
                "stage": 1,
                "order": 1,
            }
        }


class UnitOfMeasureSchema(BaseModel):
    unit_of_measure: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "unit_of_measure": "each",
            }
        }


class ItemSchema(BaseModel):
    item: str
    unit_of_measure_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "item": "Rim of paper",
                "unit_of_measure_id": 1,
            }
        }


class FinancialYearSchema(BaseModel):
    financial_year: str
    start_date: date
    end_date: date
    status: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "financial_year": "2023-2024 Financial year",
                "start_date": "2023-04-01",
                "end_date": "2024-03-31",
                "status": 1,
            }
        }


class BudgetSchema(BaseModel):
    amount: int
    department_id: int
    financial_year_id: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "amount": 120000,
                "department_id": 1,
                "financial_year_id": 1,
            }
        }


class RequestApprovalHistorySchema(BaseModel):
    request_id: int
    comment: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "request_id": 1,
                "comment": "Here is my sample comment ",
            }
        }


class RequestApprovalCommentSchema(BaseModel):
    request_approval_history_id: int
    comment: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "request_approval_history_id": 1,
                "comment": 1,
            }
        }


class ResetPasswordSchema(BaseModel):
    email: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "email": "youremail@email.com",
            }
        }


class PurchaseOrderSchema(BaseModel):
    request_id: int
    supplier_id: int
    item_id: int
    amount: int

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "request_id": 1,
                "supplier_id": 1,
                "item_id": 1,
                "amount": "1000",
            }
        }


class PurchaseOrderItemSchema(BaseModel):
    purchase_order_id: int
    request_item_id: int
    amount: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "purchase_order_id": 1,
                "request_item_id": 1,
                "amount": 1000,
            }
        }


class PurchaseOrderApprovalHistorySchema(BaseModel):
    purchase_order_id: int
    comment: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "purchase_order_id": 1,
                "comment": "Here is the comment",
            }
        }


class DistrictSchema(BaseModel):
    district: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "district": "Rumphi",
            }
        }


class BusinessEntitySchema(BaseModel):
    district_id: int
    business_category_id: int
    business_name: str
    address: str
    email: str
    phone: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "district_id": 1,
                "business_category_id": 1,
                "business_name": "RMS Pharmacy",
                "address": "P.O Box 2440, Blantyre, Malawi",
                "email": "email@gmail.com",
                "phone": "0999999990",
            }
        }


class PersonnelSchema(BaseModel):
    firstname: str
    lastname: str
    reg_number: str
    personnel_cadre_id: int
    email: str
    phone: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "firstname": "Simon",
                "lastname": "Matchado",
                "reg_number": "PMRA1234",
                "personnel_cadre_id": 1,
                "email": "email@gmail.com",
                "phone": "0999999990",
            }
        }
