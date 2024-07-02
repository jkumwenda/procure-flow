<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Edit workflow</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Edit workflow</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-2xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editWorkflow" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Workflow name
        </span>
        <input type="input" name="file category" v-model="workflowData.workflow"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Workflow name" required />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Description
        </span>
        <textarea type="textarea" name="description" v-model="workflowData.description"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Description" required></textarea>
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-2xl">
          Save
        </button>
        <router-link :to="{ name: 'Workflows' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-2xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditWorkflowView",
  data() {
    return {
      id: this.$route.params.id,
      workflowData: {
        workflow: "",
        description: "",
      },
      department: {},
      isLoading: true,
    };
  },
  mounted() {
    this.getWorkflow();
  },
  methods: {
    async editWorkflow() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "workflows",
          this.id,
          this.workflowData
        );
        this.workflow = response.data;
        this.isLoading = false;
        router.push("/workflows");
      } catch (error) {
        console.error("Error fetching file workflows:", error);
        this.isLoading = false;
      }
    },
    async getWorkflow() {
      try {
        const response = await fetchItem("workflows", this.id);
        this.workflowData.workflow = response.workflow.workflow;
        this.workflowData.description = response.workflow.description;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching workflows:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
