<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">Roles</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }"
            class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>Roles</span>
        </p>
      </div>
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 px-4 rounded-2xl shadow-sm">
        <div class="flex">
          <p class="text-2xl font-semibold">
            {{ role.role }}
          </p>
        </div>
        <div class="flex flex-col">
          <div
            class="flex flex-row space-x-2 text-sm uppercase text-dodger-blue-800 py-2 border-b border-1 border-dodger-blue-500">
            <p>Permissions</p>
            <p class="capitalize font-semibold">(click to remove)</p>
          </div>
          <div class="flex flex-row flex-wrap my-4">
            <button class="bg-dodger-blue-100 text-dodger-blue-800 rounded-xl px-4 py-1 m-1"
              v-for="assigned_permission in assigned_permissions" :key="assigned_permission.id"
              @click="deleteRolePermission(assigned_permission.id)">
              {{ assigned_permission.permission }}
            </button>
          </div>
          <div
            class="flex flex-row space-x-2 text-sm uppercase text-dodger-blue-800 py-2 border-b border-1 border-dodger-blue-500">
            <p>Permissions</p>
            <p class="capitalize font-semibold">(click to assign)</p>
          </div>
          <div class="flex flex-row flex-wrap my-4">
            <button class="bg-dodger-blue-200 text-dodger-blue-800 rounded-xl px-4 py-1 m-1"
              v-for="permission in filteredPermissions" :key="permission.id" @click="addRolePermission(permission.id)">
              {{ permission.permission }}
            </button>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchItem, fetchData, deleteItem, createItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  name: "RoleView",
  components: {
    SpinnerComponent,
  },
  data() {
    return {
      id: this.$route.params.id,
      isLoading: true,
      role: {},
      assigned_permissions: [],
      permissions: [],
      currentPage: 1,
      totalPages: "",
      pageSize: 200,
      searchPhrase: ""
    };
  },
  computed: {
    filteredPermissions() {
      return this.permissions.filter((permission) => {
        const permissionId = permission.id;
        return !this.assigned_permissions.some(
          (assigned_permission) => assigned_permission.permission_id === permissionId
        );
      });
    },
  },
  mounted() {
    this.getRole();
    this.getPermissions();
  },
  methods: {
    async getRole() {
      try {
        const response = await fetchItem("roles", this.id);
        this.role = response.role;
        this.assigned_permissions = response.permissions;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching roles:", error);
        this.isLoading = false;
      }
    },
    async getPermissions() {
      try {
        const response = await fetchData("permissions", this.currentPage, this.pageSize, this.searchPhrase);
        this.permissions = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching permissions:", error);
        this.isLoading = false;
      }
    },

    async deleteRolePermission(role_permission_id) {
      this.isLoading = true;
      try {
        await deleteItem("roles/permissions", role_permission_id);
        const index = this.assigned_permissions.findIndex((assigned_permission) => assigned_permission.id === role_permission_id);
        if (index !== -1) {
          this.assigned_permissions.splice(index, 1);
        }
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching permissions:", error);
        this.isLoading = false;
      }
      const index = this.assigned_permissions.findIndex(
        (assigned_permission) => assigned_permission.id === role_permission_id
      );
      if (index !== -1) {
        this.assigned_permissions.splice(index, 1);
      }
    },


    async addRolePermission(permissionId) {
      const rolePermissionData = {
        role_id: this.id,
        permission_id: permissionId,
      };
      this.isLoading = true;
      try {
        await createItem("roles/permissions/", rolePermissionData);
        this.getRole();
        this.getPermissions();
        this.isLoading = false;
      } catch (error) {
        console.error("Error add role permission failed:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
