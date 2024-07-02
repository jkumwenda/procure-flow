<template>
  <div class="text-xl font-semibold">Department Details</div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-2xl shadow-sm">
    <form
      class="flex flex-col w-5/12 space-y-4"
      @submit.prevent="addDepartment"
      method="POST"
    >
      <label class="block">
        <span
          class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700"
        >
          Department
        </span>
        <input
          type="input"
          name="department"
          v-model="departmentData.department"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Finance"
        />
      </label>
      <div class="flex flex-row space-x-4">
        <button
          type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-2xl"
        >
          Add department
        </button>
        <router-link
          :to="{ name: 'Departments' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-2xl"
          >Cancel</router-link
        >
      </div>
    </form>
  </div>
</template>
<script>
import { createItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "AddDepartmentView",
  data() {
    return {
      departmentData: {
        department: "",
      },
      isLoading: true,
    };
  },
  methods: {
    async addDepartment() {
      this.isLoading = true;
      try {
        const response = await createItem("departments", this.departmentData);
        this.departments = response.data;
        this.isLoading = false;
        router.push("/departments");
      } catch (error) {
        console.error("Error fetching departments:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
