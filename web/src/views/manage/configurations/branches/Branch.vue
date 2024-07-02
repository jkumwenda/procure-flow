<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else>
      <div class="flex items-center text-xl font-semibold">
        <OfficeBuildingIcon class="h-8 w-8 text-catalina-blue-500 mr-2" />
        Branch
      </div>
      <div
        class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 px-4 rounded-2xl shadow-sm"
      >
        <div class="flex">
          <p class="text-2xl font-semibold">
            {{ branch }}
          </p>
        </div>
        <div class="flex flex-col">
          <div
            class="flex flex-row space-x-2 text-sm uppercase text-dodger-blue-800 py-2 border-b border-1 border-dodger-blue-500"
          >
            <p>Departments</p>
            <p class="capitalize font-semibold">(click to remove)</p>
          </div>
          <div class="flex flex-row flex-wrap my-4">
            <button
              class="bg-dodger-blue-100 text-dodger-blue-800 rounded-xl px-4 py-1 m-1"
              v-for="assign_department in assign_departments"
              :key="assign_department.id"
              @click="removeDepartmentFromBranch(assign_department.id)"
            >
              {{ assign_department.department }}
            </button>
          </div>
          <div
            class="flex flex-row space-x-2 text-sm uppercase text-dodger-blue-800 py-2 border-b border-1 border-dodger-blue-500"
          >
            <p>Departments</p>
            <p class="capitalize font-semibold">(click to assign)</p>
          </div>
          <div class="flex flex-row flex-wrap space-x-2 my-4">
            <button
              class="bg-dodger-blue-200 text-dodger-blue-800 rounded-xl px-4 py-1 m-1"
              v-for="department in filteredDepartments"
              :key="department.id"
              @click="assignDepartmentToBranch(department.id)"
            >
              {{ department.department }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { OfficeBuildingIcon } from "@heroicons/vue/outline";
import { fetchItem, fetchData, createItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  name: "BranchView",
  components: {
    OfficeBuildingIcon,
    SpinnerComponent,
  },
  data() {
    return {
      branch: "",
      id: this.$route.params.id,
      isLoading: true,
      assign_departments: [],
      departments: [],
    };
  },
  computed: {
    filteredDepartments() {
      return this.departments.filter((department) => {
        const departmentId = department.id;
        return !this.assign_departments.some(
          (assign_department) => assign_department.id === departmentId
        );
      });
    },
  },
  mounted() {
    this.getBranchDepartments();
    this.getDepartments();
  },
  methods: {
    async getBranchDepartments() {
      try {
        const response = await fetchItem("branches/departments", this.id);
        this.branch = response.branch;
        this.assign_departments = response.departments;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching branches:", error);
        this.isLoading = false;
      }
    },
    async getDepartments() {
      try {
        const response = await fetchData("departments");
        this.departments = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching departments:", error);
        this.isLoading = false;
      }
    },
    async assignDepartmentToBranch(departmentId) {
      const branchDepartmentData = {
        branch_id: this.id,
        department_id: departmentId,
      };
      this.isLoading = true;
      try {
        await createItem("branches/departments/", branchDepartmentData);
        this.getBranchDepartments();
        this.getDepartments();
        this.isLoading = false;
      } catch (error) {
        console.error("Error assigning department to branch:", error);
        this.isLoading = false;
      }
    },
    async removeDepartmentFromBranch(departmentId) {
      const branchDepartmentData = {
        branch_id: this.id,
        department_id: departmentId,
      };
      this.isLoading = true;
      try {
        await createItem("branches/remove_department/", branchDepartmentData);
        this.getBranchDepartments();
        this.getDepartments();
        this.isLoading = false;
      } catch (error) {
        console.error("Error removing department from branch:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
