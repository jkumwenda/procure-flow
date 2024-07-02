import os
from fastapi import FastAPI
from routers import (
    auth,
    file_categories,
    branches,
    users,
    roles,
    dashboard,
    permissions,
    business_categories,
    personnel_cadres,
    positions,
    departments,
    employees,
    workflows,
    items,
    unit_of_measures,
    financial_years,
    budgets,
    requests,
    approval_actions,
    supplier_categories,
    suppliers,
    purchase_orders,
    records,
    districts,
    business_entities,
    personnels,
)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PMRA ERP API",
    description="PMRA ERP Application Programmable Interface",
    version="0.0.1",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "PowerBase INC",
        "url": "https://lojiksol.mw/contact/",
        "email": "jkumwenda@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    os.getenv("CLIENT_ORIGIN"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(dashboard.router, tags=["Dashboard"], prefix="/dashboard")
app.include_router(users.router, tags=["Users"], prefix="/users")
app.include_router(permissions.router, tags=["Permissions"], prefix="/permissions")
app.include_router(roles.router, tags=["Roles"], prefix="/roles")
app.include_router(
    file_categories.router, tags=["File Categories"], prefix="/file_categories"
)
app.include_router(
    business_categories.router,
    tags=["Business Categories"],
    prefix="/business_categories",
)
app.include_router(
    personnel_cadres.router, tags=["Personnel Cadres"], prefix="/personnel_cadres"
)
app.include_router(positions.router, tags=["Positions"], prefix="/positions")
app.include_router(branches.router, tags=["Branches"], prefix="/branches")
app.include_router(departments.router, tags=["Departments"], prefix="/departments")
app.include_router(employees.router, tags=["Employees"], prefix="/employees")
app.include_router(records.router, tags=["Records"], prefix="/records")
app.include_router(
    business_entities.router, tags=["Business entities"], prefix="/business_entities"
)
app.include_router(personnels.router, tags=["Personnels"], prefix="/personnels")

# Workflow endpoints
app.include_router(
    approval_actions.router, tags=["Approval Actions"], prefix="/approval_actions"
)
app.include_router(
    supplier_categories.router,
    tags=["Supplier Categories"],
    prefix="/supplier_categories",
)
app.include_router(
    suppliers.router,
    tags=["Suppliers"],
    prefix="/suppliers",
)
app.include_router(workflows.router, tags=["Workflows"], prefix="/workflows")
app.include_router(
    unit_of_measures.router, tags=["Unit Of Measures"], prefix="/unit_of_measures"
)
app.include_router(items.router, tags=["Items"], prefix="/items")
app.include_router(
    financial_years.router, tags=["Financial Year"], prefix="/financial_years"
)
app.include_router(budgets.router, tags=["Budget"], prefix="/budgets")
app.include_router(requests.router, tags=["Request"], prefix="/requests")
app.include_router(
    purchase_orders.router, tags=["Purchase Orders"], prefix="/purchase_orders"
)
app.include_router(districts.router, tags=["Districts"], prefix="/districts")
