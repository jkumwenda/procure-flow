<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div
      class="flex flex-col border-2 border-catalina-blue-500 border-t-8 bg-catskill-white-100 dark:bg-gray-800 rounded-xl shadow-lg w-4/12 z-50">
      <div class="border-b font-bold text-lg border-b-4 p-4 px-6 space-y-4 border-b-silver-500">
        Approval workflow details
      </div>
      <div v-if="message" class="p-4 m-6 rounded-xl text-catskill-white-100 py-2 text bg-mountain-meadow-500">{{
        message }}
      </div>
      <SpinnerComponent v-if="isLoading" />
      <form v-else class="flex flex-col block space-y-2 p-4 " @submit.prevent="editApprovalWorkflow" method="POST">
        <label class="block">
          <input type="number" name="stage" v-model="approvalWorkflowData.stage"
            class="mt-2 px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Stage number" required />
        </label>
        <label class="block">
          <input type="number" name="stage" v-model="approvalWorkflowData.order"
            class="mt-2 px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Order number" required />
        </label>
        <label class="block">
          <select name="role"
            class="mt-2 px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="approvalWorkflowData.approval_action_id">
            <option value="" disabled selected>--Select a approval action--</option>
            <option v-for="approval_action in approval_actions" :key="approval_action.id" :value="approval_action.id">
              {{ approval_action.approval_action }}
            </option>
          </select>
        </label>
        <label class="block">
          <select name="role"
            class="mt-2 px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="approvalWorkflowData.position_id">
            <option value="" disabled selected>--Select a position--</option>
            <option v-for="position in positions" :key="position.id" :value="position.id">
              {{ position.position }}
            </option>
          </select>
        </label>
        <label class="block">
          <select name="role"
            class="mt-2 px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="approvalWorkflowData.department_id">
            <option value="" disabled selected>--Select a department--</option>
            <option v-for="department in departments" :key="department.id" :value="department.id">
              {{ department.department }}
            </option>
          </select>
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Update stage
          </button>
          <button @click="close" class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Close</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchData, updateItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  components: {
    SpinnerComponent
  },
  data() {
    return {
      approvalWorkflowData: {
        workflow_id: "",
        position_id: "",
        department_id: "",
        approval_action_id: "",
        stage: "",
        order: "",
      },
      positions: {},
      departments: {},
      approval_actions: {},
      isLoading: true,
      message: "",
      currentPage: 1,
      totalPages: "",
      pageSize: 100,
      searchPhrase: ""
    };
  },

  props: {
    show: {
      type: Boolean,
      required: true,
    },
    workflow_id: {
      type: Number,
      required: true,
    },
    approval_workflow: {
      type: Object,
      required: true,
    },
  },

  mounted() {
    this.getPositions();
    this.getDepartments();
    this.getApprovalActions();
  },
  watch: {
    approval_workflow: {
      immediate: true,
      handler(newApprovalWorkflow) {
        if (newApprovalWorkflow) {
          this.loadData(newApprovalWorkflow);
        }
      },
    },
  },


  methods: {
    loadData(newApprovalWorkflow) {
      this.approvalWorkflowData = {
        workflow_id: this.workflow_id,
        position_id: newApprovalWorkflow.position_id,
        department_id: newApprovalWorkflow.department_id,
        approval_action_id: newApprovalWorkflow.approval_action_id,
        stage: newApprovalWorkflow.stage,
        order: newApprovalWorkflow.order,
      };
    },
    async getPositions() {
      try {
        const response = await fetchData("positions", this.currentPage, this.pageSize, this.searchPhrase);
        this.positions = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching positions:", error);
        this.isLoading = false;
      }
    },
    async getDepartments() {
      try {
        const response = await fetchData("departments", this.currentPage, this.pageSize, this.searchPhrase);
        this.departments = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching departments:", error);
        this.isLoading = false;
      }
    },
    async getApprovalActions() {
      try {
        const response = await fetchData("approval_actions", this.currentPage, this.pageSize, this.searchPhrase);
        this.approval_actions = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching approval actions:", error);
        this.isLoading = false;
      }
    },
    async editApprovalWorkflow() {
      this.isLoading = true;
      try {
        const response = await updateItem("workflows/approval_workflows", this.approval_workflow.id, this.approvalWorkflowData);
        this.request_item = response.data;
        this.isLoading = false;
        this.message = "Request approval workflow edited successfully";
        this.$emit("approval-workflow-added");
      } catch (error) {
        console.error("Error fetching approval workflow:", error);
        this.isLoading = false;
      }
    },

    close() {
      this.$emit("closed");
    },
  },
};
</script>
