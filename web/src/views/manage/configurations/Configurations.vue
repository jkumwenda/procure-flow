<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">System Cofigurations</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>System cofigurations</span>
    </p>
  </div>
  <div v-if="user">Logged in as {{ user.firstname }} {{ user.lastname }}</div>
  <div class="flex flex-1 sm:flex-row flex-col sm:flex-wrap flex-no-wrap">
    <router-link v-if="permissions.includes('READ_USER')" :to="{ name: 'Users' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <UsersIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Users</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('READ_ROLE')" :to="{ name: 'Roles' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Roles</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('READ_POSITION')" :to="{ name: 'Positions' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <CubeIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Employee positions</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('READ_BRANCH')" :to="{ name: 'Branches' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <OfficeBuildingIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Branches</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('READ_DEPARTMENT')" :to="{ name: 'Departments' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <CollectionIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Departments</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_APPROVAL_ACTION')" :to="{ name: 'ApprovalActions' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <TerminalIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Approval Stage Action</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_WORKFLOW')" :to="{ name: 'Workflows' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <DocumentIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Workflows</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_UNIT_OF_MEASURE')" :to="{ name: 'UnitOfMeasures' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <ScaleIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Unit of Measures</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_ITEM')" :to="{ name: 'Items' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <DuplicateIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Items</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_FINANCIAL_YEAR')" :to="{ name: 'FinancialYears' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100">
        <CalendarIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Financial year</div>
      </div>
    </router-link>

    <router-link v-if="permissions.includes('VIEW_BUDGET')" :to="{ name: 'Budgets' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100">
        <CashIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Budget</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_SUPPLIER_CATEGORY')" :to="{ name: 'SupplierCategories' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <GiftIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Supplier Categories</div>
      </div>
    </router-link>
    <router-link v-if="permissions.includes('VIEW_SUPPLIER')" :to="{ name: 'Suppliers' }"
      class="p-1 sm:w-3/12 w-12/12 justify-center items-center text-center">
      <div
        class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
        <GiftIcon class="h-8 w-8 font-light text-catalina-blue-100" />
        <div class="pl-2">Suppliers</div>
      </div>
    </router-link>
  </div>
</template>
<script>
import {
  CalendarIcon,
  UserGroupIcon,
  CubeIcon,
  OfficeBuildingIcon,
  CashIcon,
  UsersIcon,
  ScaleIcon,
  DocumentIcon,
  CollectionIcon, DuplicateIcon, TerminalIcon, GiftIcon
} from "@heroicons/vue/outline";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "ConfigurationsViewView",
  components: {
    CalendarIcon,
    UserGroupIcon,
    CubeIcon,
    OfficeBuildingIcon,
    CollectionIcon,
    DocumentIcon,
    CashIcon,
    UsersIcon,
    ScaleIcon, DuplicateIcon, TerminalIcon, GiftIcon
  },
  setup() {
    const authStore = useAuthStore()
    const loginUser = authStore.loginUser
    const permissions = authStore.permissions
    const accessToken = authStore
    return { loginUser, permissions, accessToken }
  },
  methods: {
    generateImageUrl() {
      const fileLocation = 'uploads/e2c13ab2612e48eb85f3883e8674ca18/signature.png'; // Your file location here
      const encodedLocation = encodeURIComponent(fileLocation);
      return `http://localhost:8000/show_signatures/?file_location=${encodedLocation}`;
    },
  }
};
</script>
