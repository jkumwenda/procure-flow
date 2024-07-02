<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Edit role</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Edit role</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editRole" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Role
        </span>
        <input type="input" name="role" v-model="roleData.role"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Role" required />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Description
        </span>
        <textarea type="textarea" name="description" v-model="roleData.description"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Description" required></textarea>
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'Roles' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditRoleView",
  data() {
    return {
      id: this.$route.params.id,
      roleData: {
        role: "",
        description: "",
      },
      role: {},
      isLoading: true,
    };
  },
  mounted() {
    this.getRole();
  },
  methods: {
    async editRole() {
      this.isLoading = true;
      try {
        const response = await updateItem("roles", this.id, this.roleData);
        this.role = response.data;
        this.isLoading = false;
        router.push("/roles");
      } catch (error) {
        console.error("Error fetching roles:", error);
        this.isLoading = false;
      }
    },
    async getRole() {
      try {
        const response = await fetchItem("roles", this.id);
        this.roleData.role = response.role.role;
        this.roleData.description = response.role.description;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching roles:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
