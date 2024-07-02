from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    DATE,
    text,
)
from sqlalchemy.sql.schema import Column, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import random


def generate_uuid():
    return random.randint(0, 8)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    phone = Column(String(25), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    verified = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    user_role = relationship("UserRole", back_populates="user")
    employee = relationship("Employee", back_populates="user")
    request = relationship("Request", back_populates="user")
    user_department = relationship("UserDepartment", back_populates="user")
    user_position = relationship("UserPosition", back_populates="user")
    request_approval_history = relationship(
        "RequestApprovalHistory", back_populates="user"
    )
    purchase_order_approval_history = relationship(
        "PurchaseOrderApprovalHistory", back_populates="user"
    )
    user_signature = relationship("UserSignature", back_populates="user")

    def __repr__(self):
        return f"<Users {self.users}"


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(
        String(45),
        unique=True,
    )
    description = Column(
        Text,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    user_role = relationship("UserRole", back_populates="role")
    role_permission = relationship("RolePermission", back_populates="role")

    def __repr__(self):
        return f"<Role {self.role}"


class UserSignature(Base):
    __tablename__ = "user_signature"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    user = relationship("Users", back_populates="user_signature")

    def __repr__(self):
        return f"<UserSignature {self.user_signature}"


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (UniqueConstraint(user_id, role_id, name="user_id_role_id"),)
    user = relationship("Users", back_populates="user_role")
    role = relationship("Role", back_populates="user_role")

    def __repr__(self):
        return f"<UserRole {self.user_role}"


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(
        String(45),
        unique=True,
        nullable=False,
    )
    permission_code = Column(
        String(45),
        unique=True,
        nullable=False,
    )
    system_code = Column(
        String(45),
        unique=False,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    role_permission = relationship("RolePermission", back_populates="permission")

    def __repr__(self):
        return f"<Permission {self.permission}"


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permission.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="role_id_permission_id"),
    )
    role = relationship("Role", back_populates="role_permission")
    permission = relationship("Permission", back_populates="role_permission")

    def __repr__(self):
        return f"<RolePermission {self.role_permission}"


class FileCategory(Base):
    __tablename__ = "file_category"

    id = Column(Integer, primary_key=True, index=True)
    file_category = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    employee_file = relationship(
        "EmployeeFile",
        back_populates="file_category",
    )
    business_entity_file = relationship(
        "BusinessEntityFile",
        back_populates="file_category",
    )
    department_file = relationship(
        "DepartmentFile",
        back_populates="file_category",
    )
    personnel_file = relationship(
        "PersonnelFile",
        back_populates="file_category",
    )

    def __repr__(self):
        return f"<FileCategory {self.file_category}"


class BusinessCategory(Base):
    __tablename__ = "business_category"

    id = Column(Integer, primary_key=True, index=True)
    business_category = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    business_entity = relationship(
        "BusinessEntity",
        back_populates="business_category",
    )

    def __repr__(self):
        return f"<BusinessCategory {self.business_category}"


class PersonnelCadre(Base):
    __tablename__ = "personnel_cadre"

    id = Column(Integer, primary_key=True, index=True)
    personnel_cadre = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    personnel = relationship(
        "Personnel",
        back_populates="personnel_cadre",
    )

    def __repr__(self):
        return f"<PersonnelCadre {self.personnel_cadre}"


class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    employee = relationship("Employee", back_populates="position")
    approval_workflow = relationship("ApprovalWorkflow", back_populates="position")
    user_position = relationship("UserPosition", back_populates="position")

    def __repr__(self):
        return f"<Position {self.position}"


class UserPosition(Base):
    __tablename__ = "user_position"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (
        UniqueConstraint(user_id, position_id, name="user_id_position_id"),
    )
    user = relationship("Users", back_populates="user_position")
    position = relationship("Position", back_populates="user_position")

    def __repr__(self):
        return f"<UserPosition {self.user_position}"


class Module(Base):
    __tablename__ = "module"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )

    def __repr__(self):
        return f"<Module {self.module}"


class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, index=True)
    branch = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    employee = relationship("Employee", back_populates="branch")

    def __repr__(self):
        return f"<Branch {self.branch}"


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    employee = relationship("Employee", back_populates="department")
    approval_workflow = relationship("ApprovalWorkflow", back_populates="department")
    budget = relationship("Budget", back_populates="department")
    user_department = relationship("UserDepartment", back_populates="department")
    request = relationship("Request", back_populates="department")
    department_file = relationship(
        "DepartmentFile",
        back_populates="department",
    )

    def __repr__(self):
        return f"<Department {self.department}"


class UserDepartment(Base):
    __tablename__ = "user_department"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (
        UniqueConstraint(user_id, department_id, name="user_id_department_id"),
    )
    user = relationship("Users", back_populates="user_department")
    department = relationship("Department", back_populates="user_department")

    def __repr__(self):
        return f"<UserDepartment {self.user_department}"


class BranchDepartment(Base):
    __tablename__ = "branch_department"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )

    __table_args__ = (
        UniqueConstraint("branch_id", "department_id", name="branch_id_department_id"),
    )

    def __repr__(self):
        return f"<BranchDepartment {self.branch_department}"


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    employee_number = Column(
        String(45),
        unique=True,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    user = relationship("Users", back_populates="employee")
    branch = relationship("Branch", back_populates="employee")
    department = relationship("Department", back_populates="employee")
    position = relationship("Position", back_populates="employee")
    employee_file = relationship(
        "EmployeeFile",
        back_populates="employee",
    )

    def __repr__(self):
        return f"<Employee {self.employee}"


# Workflow models
class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, index=True)
    workflow = Column(
        String(45),
        unique=True,
    )
    description = Column(
        String(255),
        unique=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    approval_workflow = relationship("ApprovalWorkflow", back_populates="workflow")

    def __repr__(self):
        return f"<Workflow {self.workflow}"


class ApprovalAction(Base):
    __tablename__ = "approval_action"

    id = Column(Integer, primary_key=True, index=True)
    approval_action = Column(String(25), nullable=False, unique=True)
    description = Column(String(255), nullable=False, unique=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    approval_workflow = relationship(
        "ApprovalWorkflow", back_populates="approval_action"
    )
    request_approval_history = relationship(
        "RequestApprovalHistory", back_populates="approval_action"
    )
    purchase_order_approval_history = relationship(
        "PurchaseOrderApprovalHistory", back_populates="approval_action"
    )

    def __repr__(self):
        return f"<ApprovalAction {self.approval_action}"


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(
        String(45),
        unique=True,
    )
    address = Column(
        Text,
        nullable=False,
    )
    email = Column(
        String(45),
        unique=False,
    )
    phone = Column(
        String(45),
        unique=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    supplier_supplier_category = relationship(
        "SupplierSupplierCategory", back_populates="supplier"
    )
    purchase_order = relationship("PurchaseOrder", back_populates="supplier")

    def __repr__(self):
        return f"<Role {self.supplier}"


class SupplierCategory(Base):
    __tablename__ = "supplier_category"

    id = Column(Integer, primary_key=True, index=True)
    supplier_category = Column(String(25), nullable=False, unique=True)
    description = Column(String(255), nullable=False, unique=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )

    supplier_supplier_category = relationship(
        "SupplierSupplierCategory", back_populates="supplier_category"
    )

    def __repr__(self):
        return f"<SupplierCategory {self.supplier_category}"


class SupplierSupplierCategory(Base):
    __tablename__ = "supplier_supplier_category"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    supplier_category_id = Column(
        Integer, ForeignKey("supplier_category.id"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (
        UniqueConstraint(
            "supplier_id",
            "supplier_category_id",
            name="supplier_id_supplier_category_id",
        ),
    )
    supplier = relationship("Supplier", back_populates="supplier_supplier_category")
    supplier_category = relationship(
        "SupplierCategory", back_populates="supplier_supplier_category"
    )

    def __repr__(self):
        return f"<SupplierSupplierCategory {self.supplier_supplier_category}"


class ApprovalWorkflow(Base):
    __tablename__ = "approval_workflow"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflow.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    approval_action_id = Column(
        Integer, ForeignKey("approval_action.id"), nullable=False
    )
    stage = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    workflow = relationship("Workflow", back_populates="approval_workflow")
    department = relationship("Department", back_populates="approval_workflow")
    position = relationship("Position", back_populates="approval_workflow")
    approval_action = relationship("ApprovalAction", back_populates="approval_workflow")

    def __repr__(self):
        return f"<ApprovalWorkflow {self.approval_workflow}"


class FinancialYear(Base):
    __tablename__ = "financial_year"

    id = Column(Integer, primary_key=True, index=True)
    financial_year = Column(String(255), nullable=False, unique=True)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    budget = relationship("Budget", back_populates="financial_year")

    def __repr__(self):
        return f"<FinancialYear {self.financial_year}"


class Budget(Base):
    __tablename__ = "budget"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    financial_year_id = Column(Integer, ForeignKey("financial_year.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    financial_year = relationship("FinancialYear", back_populates="budget")
    department = relationship("Department", back_populates="budget")

    def __repr__(self):
        return f"<Budget {self.budget}"


class UnitOfMeasure(Base):
    __tablename__ = "unit_of_measure"

    id = Column(Integer, primary_key=True, index=True)
    unit_of_measure = Column(String(25), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    item = relationship("Item", back_populates="unit_of_measure")

    def __repr__(self):
        return f"<UnitOfMeasure {self.unit_of_measure}"


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String(255), nullable=False, unique=True)
    unit_of_measure_id = Column(
        Integer, ForeignKey("unit_of_measure.id"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )

    unit_of_measure = relationship("UnitOfMeasure", back_populates="item")
    request_item = relationship("RequestItem", back_populates="item")

    def __repr__(self):
        return f"<Item {self.item}"


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    request = Column(String(255), nullable=False, unique=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    request_status = Column(Integer, nullable=False)
    request_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    user = relationship("Users", back_populates="request")
    department = relationship("Department", back_populates="request")
    request_item = relationship("RequestItem", back_populates="request")
    request_file = relationship("RequestFile", back_populates="request")
    request_approval_history = relationship(
        "RequestApprovalHistory", back_populates="request"
    )
    purchase_order = relationship("PurchaseOrder", back_populates="request")

    def __repr__(self):
        return f"<Request {self.request}"


class RequestItem(Base):
    __tablename__ = "request_item"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("request.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    request = relationship("Request", back_populates="request_item")
    item = relationship("Item", back_populates="request_item")
    purchase_order_item = relationship(
        "PurchaseOrderItem", back_populates="request_item"
    )

    def __repr__(self):
        return f"<RequestItem {self.request_item}"


class RequestFile(Base):
    __tablename__ = "request_file"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(Text, nullable=False)
    real_file_name = Column(Text, nullable=False)
    request_id = Column(Integer, ForeignKey("request.id"), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    request = relationship("Request", back_populates="request_file")

    def __repr__(self):
        return f"<RequestFile {self.request_file}"


class RequestApprovalHistory(Base):
    __tablename__ = "request_approval_history"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("request.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_action_id = Column(
        Integer, ForeignKey("approval_action.id"), nullable=False
    )
    approval_status = Column(Integer, nullable=False)
    next_stage = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    request = relationship("Request", back_populates="request_approval_history")
    approval_action = relationship(
        "ApprovalAction", back_populates="request_approval_history"
    )
    user = relationship("Users", back_populates="request_approval_history")
    approval_history_comment = relationship(
        "ApprovalHistoryComment", back_populates="request_approval_history"
    )

    def __repr__(self):
        return f"<RequestApprovalHistory {self.request_approval_history}"


class ApprovalHistoryComment(Base):
    __tablename__ = "approval_history_comment"

    id = Column(Integer, primary_key=True, index=True)
    request_approval_history_id = Column(
        Integer, ForeignKey("request_approval_history.id"), nullable=False
    )
    comment = Column(
        Text,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    request_approval_history = relationship(
        "RequestApprovalHistory", back_populates="approval_history_comment"
    )

    def __repr__(self):
        return f"<ApprovalHistoryComment {self.approval_history_comment}"


class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("request.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    raiser_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    purchase_order_status = Column(Integer, nullable=False)
    purchase_order_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    request = relationship("Request", back_populates="purchase_order")
    supplier = relationship("Supplier", back_populates="purchase_order")
    purchase_order_approval_history = relationship(
        "PurchaseOrderApprovalHistory", back_populates="purchase_order"
    )
    purchase_order_item = relationship(
        "PurchaseOrderItem", back_populates="purchase_order"
    )

    def __repr__(self):
        return f"<PurchaseOrder {self.purchase_order}"


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_item"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_order.id"), nullable=False)
    request_item_id = Column(Integer, ForeignKey("request_item.id"), nullable=False)
    amount = Column(String(25), nullable=False, unique=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    purchase_order = relationship("PurchaseOrder", back_populates="purchase_order_item")
    request_item = relationship("RequestItem", back_populates="purchase_order_item")

    def __repr__(self):
        return f"<PurchaseOrderItem {self.purchase_order_item}"


class PurchaseOrderApprovalHistory(Base):
    __tablename__ = "purchase_order_approval_history"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_order.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_action_id = Column(
        Integer, ForeignKey("approval_action.id"), nullable=False
    )
    approval_status = Column(Integer, nullable=False)
    next_stage = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    purchase_order = relationship(
        "PurchaseOrder", back_populates="purchase_order_approval_history"
    )
    approval_action = relationship(
        "ApprovalAction", back_populates="purchase_order_approval_history"
    )
    user = relationship("Users", back_populates="purchase_order_approval_history")
    purchase_order_approval_history_comment = relationship(
        "PurchaseOrderApprovalHistoryComment",
        back_populates="purchase_order_approval_history",
    )

    def __repr__(self):
        return f"<PurchaseOrderApprovalHistory {self.purchase_order_approval_history}"


class PurchaseOrderApprovalHistoryComment(Base):
    __tablename__ = "purchase_order_approval_history_comment"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_approval_history_id = Column(
        Integer, ForeignKey("purchase_order_approval_history.id"), nullable=False
    )
    comment = Column(
        Text,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    purchase_order_approval_history = relationship(
        "PurchaseOrderApprovalHistory",
        back_populates="purchase_order_approval_history_comment",
    )

    def __repr__(self):
        return f"<PurchaseOrderApprovalHistoryComment {self.purchase_order_approval_history_comment}"


class EmployeeFile(Base):
    __tablename__ = "employee_file"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    file_category_id = Column(Integer, ForeignKey("file_category.id"), nullable=False)
    file_name = Column(Text, nullable=False)
    real_file_name = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    access_level = Column(Integer, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    employee = relationship(
        "Employee",
        back_populates="employee_file",
    )
    file_category = relationship(
        "FileCategory",
        back_populates="employee_file",
    )

    def __repr__(self):
        return f"<EmployeeFile {self.employee_file}"


class BusinessEntity(Base):
    __tablename__ = "business_entity"

    id = Column(Integer, primary_key=True, index=True)
    business_category_id = Column(
        Integer, ForeignKey("business_category.id"), nullable=False
    )
    district_id = Column(Integer, ForeignKey("district.id"), nullable=False)
    business_category_id = Column(
        Integer, ForeignKey("business_category.id"), nullable=False
    )
    business_name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    business_category = relationship(
        "BusinessCategory",
        back_populates="business_entity",
    )
    business_entity_file = relationship(
        "BusinessEntityFile",
        back_populates="business_entity",
    )
    district = relationship(
        "District",
        back_populates="business_entity",
    )

    def __repr__(self):
        return f"<BusinessEntity {self.business_entity}"


class BusinessEntityFile(Base):
    __tablename__ = "business_entity_file"

    id = Column(Integer, primary_key=True, index=True)
    business_entity_id = Column(
        Integer, ForeignKey("business_entity.id"), nullable=False
    )
    file_category_id = Column(Integer, ForeignKey("file_category.id"), nullable=False)
    file_name = Column(Text, nullable=False)
    real_file_name = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    access_level = Column(Integer, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    business_entity = relationship(
        "BusinessEntity",
        back_populates="business_entity_file",
    )
    file_category = relationship(
        "FileCategory",
        back_populates="business_entity_file",
    )

    def __repr__(self):
        return f"<BusinessEntityFile {self.business_entity_file}"


class DepartmentFile(Base):
    __tablename__ = "department_file"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    file_category_id = Column(Integer, ForeignKey("file_category.id"), nullable=False)
    file_name = Column(Text, nullable=False)
    real_file_name = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    access_level = Column(Integer, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    department = relationship(
        "Department",
        back_populates="department_file",
    )
    file_category = relationship(
        "FileCategory",
        back_populates="department_file",
    )

    def __repr__(self):
        return f"<DepartmentFile {self.department_file}"


class District(Base):
    __tablename__ = "district"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    business_entity = relationship(
        "BusinessEntity",
        back_populates="district",
    )

    def __repr__(self):
        return f"<District {self.district}"


class Personnel(Base):
    __tablename__ = "personnel"

    id = Column(Integer, primary_key=True, index=True)
    personnel_cadre_id = Column(
        Integer, ForeignKey("personnel_cadre.id"), nullable=False
    )
    personnel_cadre_id = Column(
        Integer, ForeignKey("personnel_cadre.id"), nullable=False
    )
    firstname = Column(Text, nullable=False)
    lastname = Column(Text, nullable=False)
    reg_number = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    personnel_cadre = relationship(
        "PersonnelCadre",
        back_populates="personnel",
    )
    personnel_file = relationship(
        "PersonnelFile",
        back_populates="personnel",
    )

    def __repr__(self):
        return f"<Personnel {self.personnel}"


class PersonnelFile(Base):
    __tablename__ = "personnel_file"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id"), nullable=False)
    file_category_id = Column(Integer, ForeignKey("file_category.id"), nullable=False)
    file_name = Column(Text, nullable=False)
    real_file_name = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    access_level = Column(Integer, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    personnel = relationship(
        "Personnel",
        back_populates="personnel_file",
    )
    file_category = relationship(
        "FileCategory",
        back_populates="personnel_file",
    )

    def __repr__(self):
        return f"<PersonnelFile {self.personnel_file}"
