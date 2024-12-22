import { createRouter, createWebHashHistory } from "vue-router";
import AuthLayout from "@/layouts/AuthLayout.vue";
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import { setAuthToken } from "@/services/apiService";
import { useAuthStore } from "@/store/authStore";

const routeComponents = {
  AuthLayout,
  DefaultLayout,
  SignUpView: () => import("@/views/auth/Signup.vue"),
  ResetPasswordView: () => import("@/views/auth/ResetPassword.vue"),
  DashboardView: () => import("@/views/dashboard/Dashboard.vue"),
  RequestsView: () => import("@/views/requests/Requests.vue"),
  RequestView: () => import("@/views/requests/Request.vue"),
  AddRequestView: () => import("@/views/requests/Add.vue"),
  EditRequestView: () => import("@/views/requests/Edit.vue"),
  MyRequestsView: () => import("@/views/requests/MyRequests.vue"),
  RequestNotificationsView: () =>
    import("@/views/requests/RequestNotifications.vue"),
  GeneratePOView: () => import("@/views/requests/GeneratePO.vue"),
  PurchaseOrderView: () => import("@/views/requests/PurchaseOrder.vue"),
  UsersView: () => import("@/views/manage/users/Users.vue"),
  AddUserView: () => import("@/views/manage/users/Add.vue"),
  UserView: () => import("@/views/manage/users/User.vue"),
  EditUserView: () => import("@/views/manage/users/Edit.vue"),
  MyProfileView: () => import("@/views/manage/users/MyProfile.vue"),
  RolesView: () => import("@/views/manage/roles/Roles.vue"),
  AddRoleView: () => import("@/views/manage/roles/Add.vue"),
  EditRoleView: () => import("@/views/manage/roles/Edit.vue"),
  RoleView: () => import("@/views/manage/roles/Role.vue"),
  ConfigurationsView: () =>
    import("@/views/manage/configurations/Configurations.vue"),
  PositionsView: () =>
    import("@/views/manage/configurations/positions/Positions.vue"),
  AddPositionView: () =>
    import("@/views/manage/configurations/positions/Add.vue"),
  EditPositionView: () =>
    import("@/views/manage/configurations/positions/Edit.vue"),
  BranchesView: () =>
    import("@/views/manage/configurations/branches/Branches.vue"),
  AddBranchView: () => import("@/views/manage/configurations/branches/Add.vue"),
  EditBranchView: () =>
    import("@/views/manage/configurations/branches/Edit.vue"),
  BranchView: () => import("@/views/manage/configurations/branches/Branch.vue"),
  DepartmentsView: () =>
    import("@/views/manage/configurations/departments/Departments.vue"),
  AddDepartmentView: () =>
    import("@/views/manage/configurations/departments/Add.vue"),
  EditDepartmentView: () =>
    import("@/views/manage/configurations/departments/Edit.vue"),
  WorkflowsView: () =>
    import("@/views/manage/configurations/workflows/Workflows.vue"),
  AddWorkflowView: () =>
    import("@/views/manage/configurations/workflows/Add.vue"),
  EditWorkflowView: () =>
    import("@/views/manage/configurations/workflows/Edit.vue"),
  ApprovalActionsView: () =>
    import(
      "@/views/manage/configurations/approval-actions/ApprovalActions.vue"
    ),
  AddApprovalActionView: () =>
    import("@/views/manage/configurations/approval-actions/Add.vue"),
  EditApprovalActionView: () =>
    import("@/views/manage/configurations/approval-actions/Edit.vue"),
  SuppliersView: () =>
    import("@/views/manage/configurations/suppliers/Suppliers.vue"),
  AddSupplierView: () =>
    import("@/views/manage/configurations/suppliers/Add.vue"),
  EditSupplierView: () =>
    import("@/views/manage/configurations/suppliers/Edit.vue"),
  SupplierView: () =>
    import("@/views/manage/configurations/suppliers/Supplier.vue"),
  SupplierCategoriesView: () =>
    import(
      "@/views/manage/configurations/supplier-categories/SupplierCategories.vue"
    ),
  AddSupplierCategoryView: () =>
    import("@/views/manage/configurations/supplier-categories/Add.vue"),
  EditSupplierCategoryView: () =>
    import("@/views/manage/configurations/supplier-categories/Edit.vue"),
  WorkflowView: () =>
    import("@/views/manage/configurations/workflows/Workflow.vue"),
  itemsView: () => import("@/views/manage/configurations/items/Items.vue"),
  AddItemView: () => import("@/views/manage/configurations/items/Add.vue"),
  EditItemView: () => import("@/views/manage/configurations/items/Edit.vue"),
  FinancialYearsView: () =>
    import("@/views/manage/configurations/financial-years/FinancialYears.vue"),
  AddFinancialYearView: () =>
    import("@/views/manage/configurations/financial-years/Add.vue"),
  EditFinancialYearView: () =>
    import("@/views/manage/configurations/financial-years/Edit.vue"),
  BudgetsView: () =>
    import("@/views/manage/configurations/budgets/Budgets.vue"),
  AddBudgetView: () => import("@/views/manage/configurations/budgets/Add.vue"),
  EditBudgetView: () =>
    import("@/views/manage/configurations/budgets/Edit.vue"),
  UnitOfMeasuresView: () =>
    import("@/views/manage/configurations/unit-of-measures/UnitOfMeasures.vue"),
  AddUnitOfMeasureView: () =>
    import("@/views/manage/configurations/unit-of-measures/Add.vue"),
  EditUnitOfMeasureView: () =>
    import("@/views/manage/configurations/unit-of-measures/Edit.vue"),
};

// Define your route configurations
const routes = [
  {
    path: "/",
    name: "Auth",
    component: routeComponents.AuthLayout,
    children: [
      {
        path: "/",
        name: "Login",
        component: () => import("@/views/auth/Login.vue"),
      },
      {
        path: "/signup",
        name: "SignUp",
        component: routeComponents.SignUpView,
      },
      {
        path: "/reset-password",
        name: "ResetPassword",
        component: routeComponents.ResetPasswordView,
      },
    ],
  },
  {
    path: "/",
    name: "Main",
    component: routeComponents.DefaultLayout,
    children: [
      {
        path: "/dashboard",
        name: "Dashboard",
        component: routeComponents.DashboardView,
      },
      {
        path: "/requests",
        name: "Requests",
        component: routeComponents.RequestsView,
      },
      {
        path: "/request/:id",
        name: "Request",
        component: routeComponents.RequestView,
      },
      {
        path: "/add-request",
        name: "AddRequest",
        component: routeComponents.AddRequestView,
      },
      {
        path: "/edit-request/:id",
        name: "EditRequest",
        component: routeComponents.EditRequestView,
      },
      {
        path: "/my-request",
        name: "MyRequests",
        component: routeComponents.MyRequestsView,
      },
      {
        path: "/request-notifications",
        name: "RequestNotifications",
        component: routeComponents.RequestNotificationsView,
      },
      { path: "/users", name: "Users", component: routeComponents.UsersView },
      {
        path: "/add-user",
        name: "AddUser",
        component: routeComponents.AddUserView,
      },
      {
        path: "/user/:id",
        name: "User",
        component: routeComponents.UserView,
      },
      {
        path: "/edit-user/:id",
        name: "EditUser",
        component: routeComponents.EditUserView,
      },
      {
        path: "/my-profile/:id",
        name: "MyProfile",
        component: routeComponents.MyProfileView,
      },
      { path: "/roles", name: "Roles", component: routeComponents.RolesView },
      {
        path: "/add-role",
        name: "AddRole",
        component: routeComponents.AddRoleView,
      },
      {
        path: "/edit-role/:id",
        name: "EditRole",
        component: routeComponents.EditRoleView,
      },
      {
        path: "/role/:id",
        name: "Role",
        component: routeComponents.RoleView,
      },
      {
        path: "/configurations",
        name: "Configurations",
        component: routeComponents.ConfigurationsView,
      },

      {
        path: "/positions",
        name: "Positions",
        component: routeComponents.PositionsView,
      },
      {
        path: "/add-position",
        name: "AddPosition",
        component: routeComponents.AddPositionView,
      },
      {
        path: "/edit-position/:id",
        name: "EditPosition",
        component: routeComponents.EditPositionView,
      },
      {
        path: "/branches",
        name: "Branches",
        component: routeComponents.BranchesView,
      },
      {
        path: "/add-branch",
        name: "AddBranch",
        component: routeComponents.AddBranchView,
      },
      {
        path: "/edit-branch/:id",
        name: "EditBranch",
        component: routeComponents.EditBranchView,
      },
      {
        path: "/branch/:id",
        name: "Branch",
        component: routeComponents.BranchView,
      },
      {
        path: "/departments",
        name: "Departments",
        component: routeComponents.DepartmentsView,
      },
      {
        path: "/add-department",
        name: "AddDepartment",
        component: routeComponents.AddDepartmentView,
      },
      {
        path: "/edit-department/:id",
        name: "EditDepartment",
        component: routeComponents.EditDepartmentView,
      },
      {
        path: "/workflows",
        name: "Workflows",
        component: routeComponents.WorkflowsView,
      },
      {
        path: "/add-workflow",
        name: "AddWorkflow",
        component: routeComponents.AddWorkflowView,
      },
      {
        path: "/edit-workflow/:id",
        name: "EditWorkflow",
        component: routeComponents.EditWorkflowView,
      },
      {
        path: "/workflow/:id",
        name: "Workflow",
        component: routeComponents.WorkflowView,
      },
      {
        path: "/approval-actions",
        name: "ApprovalActions",
        component: routeComponents.ApprovalActionsView,
      },
      {
        path: "/add-approval-action",
        name: "AddApprovalAction",
        component: routeComponents.AddApprovalActionView,
      },
      {
        path: "/edit-approval-action/:id",
        name: "EditApprovalAction",
        component: routeComponents.EditApprovalActionView,
      },

      {
        path: "/suppliers",
        name: "Suppliers",
        component: routeComponents.SuppliersView,
      },
      {
        path: "/add-supplier",
        name: "AddSupplier",
        component: routeComponents.AddSupplierView,
      },
      {
        path: "/edit-supplier/:id",
        name: "EditSupplier",
        component: routeComponents.EditSupplierView,
      },
      {
        path: "/supplier/:id",
        name: "Supplier",
        component: routeComponents.SupplierView,
      },
      {
        path: "/supplier-categories",
        name: "SupplierCategories",
        component: routeComponents.SupplierCategoriesView,
      },
      {
        path: "/add-supplier-category",
        name: "AddSupplierCategory",
        component: routeComponents.AddSupplierCategoryView,
      },
      {
        path: "/edit-supplier-category/:id",
        name: "EditSupplierCategory",
        component: routeComponents.EditSupplierCategoryView,
      },

      {
        path: "/items",
        name: "Items",
        component: routeComponents.itemsView,
      },
      {
        path: "/add-item",
        name: "AddItem",
        component: routeComponents.AddItemView,
      },
      {
        path: "/edit-item/:id",
        name: "EditItem",
        component: routeComponents.EditItemView,
      },

      {
        path: "/budgets",
        name: "Budgets",
        component: routeComponents.BudgetsView,
      },
      {
        path: "/add-budget",
        name: "AddBudget",
        component: routeComponents.AddBudgetView,
      },
      {
        path: "/edit-budget/:id",
        name: "EditBudget",
        component: routeComponents.EditBudgetView,
      },

      {
        path: "/financial-years",
        name: "FinancialYears",
        component: routeComponents.FinancialYearsView,
      },
      {
        path: "/add-financial-year",
        name: "AddFinancialYear",
        component: routeComponents.AddFinancialYearView,
      },
      {
        path: "/edit-financial-year/:id",
        name: "EditFinancialYear",
        component: routeComponents.EditFinancialYearView,
      },

      {
        path: "/unit-of-measures",
        name: "UnitOfMeasures",
        component: routeComponents.UnitOfMeasuresView,
      },
      {
        path: "/add-unit-of-measure",
        name: "AddUnitOfMeasure",
        component: routeComponents.AddUnitOfMeasureView,
      },
      {
        path: "/edit-unit-of-measure/:id",
        name: "EditUnitOfMeasure",
        component: routeComponents.EditUnitOfMeasureView,
      },
      {
        path: "/generate-po/:id",
        name: "GeneratePO",
        component: routeComponents.GeneratePOView,
      },
      {
        path: "/purchase-order/:id",
        name: "PurchaseOrder",
        component: routeComponents.PurchaseOrderView,
      },
    ],
  },
  { path: "/:catchAll(.*)", name: "NotFound", component: NotFoundView },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.name === "Main")) {
    const authStore = useAuthStore();
    if (!authStore.accessToken) {
      return next("/");
    }
    setAuthToken();
    return next();
  }
  return next();
});

export default router;
