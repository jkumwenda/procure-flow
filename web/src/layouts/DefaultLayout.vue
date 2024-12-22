<template>
  <div class="flex sm:flex-row flex-col min-h-screen z-1">
    <div class="sm:w-2/12 w-12/12 bg-catalina-blue-500 border-r border-silver-400 text-catskill-white-100">
      <div class="flex py-6 flex-col space-y-4">
        <router-link :to="{ name: 'Dashboard' }" class="flex justify-center items-center p-1">
          <img alt="Vue logo" class="w-28 p-2 rounded-xl bg-catskill-white-100" src="@/assets/logo.png" />
        </router-link>
        <div class="space-y-1">
          <router-link v-if="permissions.includes('VIEW_DASHBOARD')" :to="{ name: 'Dashboard' }"
            :class="{ 'bg-catalina-blue-50': $route.name === 'Dashboard' }"
            class="flex items-center p-3 mr-3 text-md  font-roboto-light rounded-tr-xl rounded-br-xl">
            <HomeIcon class="h-6 w-6 mr-2 stroke-1" />
            Dashboard
          </router-link>
          <router-link v-if="permissions.includes('VIEW_REQUEST')" :to="{ name: 'Requests' }"
            :class="{ 'bg-catalina-blue-50': ['Requests', 'EditRequest', 'Request', 'RequestNotifications'].includes($route.name) }"
            class="flex items-center p-3 mr-3 text-m  font-roboto-light rounded-tr-xl rounded-br-xl hover:bg-catalina-blue-50">
            <TableIcon class="h-6 w-6 mr-2 stroke-1" />
            Requests
          </router-link>
          <router-link :to="{ name: 'MyRequests' }" :class="{ 'bg-catalina-blue-50': $route.name === 'MyRequests' }"
            class="flex items-center p-3 mr-3 text-m  font-roboto-light rounded-tr-xl rounded-br-xl hover:bg-catalina-blue-50">
            <ViewGridIcon class="h-6 w-6 mr-2 stroke-1" />
            My Requests
          </router-link>
          <router-link v-if="permissions.includes('ADD_REQUEST')" :to="{ name: 'AddRequest' }"
            :class="{ 'bg-catalina-blue-50': ['AddRequest'].includes($route.name) }"
            class="flex items-center p-3 mr-3 text-m  font-roboto-light rounded-tr-xl rounded-br-xl hover:bg-catalina-blue-50">
            <ViewGridAddIcon class="h-6 w-6 mr-2 stroke-1" />
            Create Request
          </router-link>
        </div>
        <div v-if="permissions.includes('ADMIN_SETTINGS')" class="mb-10">
          <h3 class="p-3 pl-4 mb-3 uppercase border-b border-silver-500">
            Admin Settings
          </h3>
          <div class="">
            <router-link v-if="permissions.includes('READ_USER')" :to="{ name: 'Users' }"
              :class="{ 'bg-catalina-blue-50': ['Users', 'AddUser', 'EditUser', 'User'].includes($route.name) }"
              class="flex items-center p-3 mr-3 text-m  font-roboto-light rounded-tr-xl rounded-br-xl hover:bg-catalina-blue-50">
              <UsersIcon class="h-6 w-6 mr-2 stroke-1" />
              Users
            </router-link>
            <router-link v-if="permissions.includes('READ_ROLE')" :to="{ name: 'Roles' }"
              :class="{ 'bg-catalina-blue-50': ['Roles', 'AddRole', 'EditRol', 'Role'].includes($route.name) }"
              class="flex items-center p-3 mr-3 text-m  font-roboto-light rounded-tr-xl rounded-br-xl hover:bg-catalina-blue-50">
              <UserGroupIcon class="h-6 w-6 mr-2 stroke-1" />
              Roles
            </router-link>
            <router-link v-if="permissions.includes('SYSTEM_CONFIGURATIONS')" :to="{ name: 'Configurations' }"
              :class="{ 'bg-catalina-blue-50': $route.name === 'Configurations' }"
              class="flex items-center p-3 mr-3 text-m  font-roboto-light rounded-tr-xl rounded-br-xl hover:bg-catalina-blue-50">
              <CogIcon class="h-6 w-6 mr-2 stroke-1" />
              Configurations
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col h-screen flex-1 space-y-4 p-4 justify-center">
      <div class="flex flex-row space-x-4 bg-catskill-white-100 shadow-sm p-4 rounded-xl">
        <div class="flex-1 bg-catskill-white-100">
          <MenuIcon class="h-6 w-6 text-red-500 mr-2" />
        </div>
        <div v-if="user">Logged in as {{ user.firstname }} {{ user.lastname }}</div>
        <div class="flex relative">
          <router-link :to="{ name: 'RequestNotifications' }"
            class="mr-4 h-6 w-6 bg-flamingo-500 text-catskill-white-100 text-white rounded-full flex items-center justify-center text-xs font-bold">
            {{ count }}
          </router-link>

          | {{ formattedCurrentDateTime }} |
        </div>
        <div class="flex">
          <UserCircleIcon class="h-6 w-6 text-catalina-blue-100 mr-2" />
          <DropdownComponent :label="`${firstname} ${lastname}`"></DropdownComponent>
        </div>
      </div>
      <div class="flex-grow space-y-4 overflow-auto">
        <router-view></router-view>
      </div>
      <div class="border-t border-silver-500 border-text-sm pt-4">
        &copy; All rights reserved
      </div>
    </div>
  </div>
</template>
<script>
import {
  HomeIcon, ViewGridAddIcon,
  UsersIcon,
  UserGroupIcon,
  CogIcon,
  UserCircleIcon,
  TableIcon, ViewGridIcon, MenuIcon
} from "@heroicons/vue/outline";
import DropdownComponent from "@/components/Dropdown";
import { fetchData } from "@/services/apiService";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "DefaultLayout",
  components: {
    HomeIcon,
    UsersIcon,
    CogIcon,
    UserGroupIcon,
    UserCircleIcon,
    ViewGridAddIcon,
    TableIcon, MenuIcon,
    DropdownComponent, ViewGridIcon,
  },
  data() {
    return {
      dropdownItems: [
        { text: "Profile", method: "profile" },
        { text: "Logout", method: "logout" },
      ],
      currentDate: new Date(),
      firstname: "",
      lastname: "",
      count: 0,
    };
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async getRequestsNotifications() {
      this.isLoading = true;
      try {
        const response = await fetchData("requests/notifications/");
        this.count = response.total_approvals;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
      }
    },
  },
  computed: {
    formattedCurrentDateTime() {
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        // hour: '2-digit',
        // minute: '2-digit',
        // second: '2-digit',
      };

      return this.currentDate.toLocaleString('en-UK', options);
    },
  },
};
</script>
