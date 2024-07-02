<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Workflow</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Workflow</span>
    </p>
  </div>
  <div class="flex flex-1 space-x-4">
    <div class="w-4/12">
      <div class="bg-catskill-white-100  rounded-xl shadow-sm">
        <h1 class="text-xl px-4 pt-4 font-bold">Workflow</h1>
        <p class="px-4 py-2 text-md border-b border-b-silver-600 pb-2">
          {{ workflow.workflow }}
        </p>
        <h1 class="text-xl px-4 pt-4 font-bold">Description</h1>
        <p class="px-4 py-2 pb-4 text-sm">{{ workflow.description }}</p>
      </div>
      <button v-if="permissions.includes('ADD_WORKFLOW')" @click="showAddApprovalWorkflow" class="my-4 bg-dodger-blue-300 hover:bg-dodger-blue-500
        text-dodger-blue-800 rounded-xl px-4 py-2">
        Add approval stage
      </button>
    </div>
    <div class="flex flex-col space-y-1 w-5/12 ">
      <div v-for="approvalWorkflow in approvalWorkflows" :key="approvalWorkflow.id">
        <div
          class="flex flex-row space-x-1 bg-catskill-white-100  rounded-2xl p-1 border-2 border-catalina-blue-500 shadow-sm">
          <div class="text-catskill-white-100 bg-catalina-blue-500 rounded-xl p-3 text-md">{{
            approvalWorkflow.stage
          }}</div>
          <div class="flex flex-1 items-center px-3">
            <div>{{ approvalWorkflow.position }}</div>
          </div>
          <div class="flex justify-center items-center w-2/12 flex justify-end">
            <PencilAltIcon v-if="permissions.includes('UPDATE_WORKFLOW')"
              @click="showEditApprovalWorkflow(approvalWorkflow)"
              class="h-6 w-6 font-bold text-dodger-blue-500 cursor-pointer">
            </PencilAltIcon>
            <TrashIcon v-if="permissions.includes('DELETE_WORKFLOW')" @click="showDeleteConfirmation(approvalWorkflow.id)"
              class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer">
            </TrashIcon>
          </div>
        </div>
        <div class="flex justify-center">
          <ArrowDownIcon class="h-8 w-8 text-catalina-blue-500 mr-2" />
        </div>
      </div>
      <div class="flex justify-center">
        <div class="bg-catalina-blue text-catskill-white-100 p-4 mr-2 rounded-full">End</div>
      </div>
    </div>
    <add-approval-workflow-modal :show="showAddApprovalWorkflowModal" @confirmed="confirmAddApprovalWorkflow"
      @closed="cancelAddApprovalWorkflow" :workflow_id="workflow.id" @approval-workflow-added="refreshWorkflows">
    </add-approval-workflow-modal>

    <edit-approval-workflow-modal :show="showEditApprovalWorkflowModal" @confirmed="confirmEditApprovalWorkflow"
      @closed="cancelEditApprovalWorkflow" :workflow_id="workflow.id" :approval_workflow="approval_workflow"
      @approval-workflow-added="refreshWorkflows">
    </edit-approval-workflow-modal>

    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteApprovalWorkflow(deleteApprovalWorkflowId)"
      @canceled="cancelDelete"></delete-confirmation-modal>
  </div>
</template>
<script>

import {
  TrashIcon,
  PencilAltIcon, ArrowDownIcon
} from "@heroicons/vue/outline";
import { fetchItem, deleteItem } from "@/services/apiService";
import AddApprovalWorkflowModal from "@/components/AddApprovalWorkflowModal.vue";
import EditApprovalWorkflowModal from "@/components/EditApprovalWorkflowModal.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "WorkflowView",
  components: {
    ArrowDownIcon,
    TrashIcon,
    PencilAltIcon,
    AddApprovalWorkflowModal,
    EditApprovalWorkflowModal,
    DeleteConfirmationModal,
  },
  data() {
    return {
      id: this.$route.params.id,
      workflow: {},
      approvalWorkflows: {},
      isLoading: true,
      departments: {},
      positions: {},
      showAddApprovalWorkflowModal: false,
      showEditApprovalWorkflowModal: false,
      showDeleteModal: false,
      approval_workflow: {},
      deleteApprovalWorkflowId: null
    };
  },
  mounted() {
    this.getWorkflow();
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async refreshWorkflows() {
      await this.getWorkflow();
    },
    async getWorkflow() {
      try {
        const response = await fetchItem("workflows", this.id);
        this.workflow = response.workflow
        this.approvalWorkflows = response.approval_workflows
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching workflow:", error);
        this.isLoading = false;
      }
    },

    async deleteApprovalWorkflow(id) {
      this.isLoading = true;
      try {
        await deleteItem("workflows/approval_workflows", id);
        const index = this.approvalWorkflows.findIndex((approvalWorkflow) => approvalWorkflow.id === id);
        if (index !== -1) {
          this.approvalWorkflows.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching approval workflows:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },

    showAddApprovalWorkflow() {
      this.showAddApprovalWorkflowModal = true;
    },
    confirmAddApprovalWorkflow() {
      this.showAddApprovalWorkflowModal = false;
    },
    cancelAddApprovalWorkflow() {
      this.showAddApprovalWorkflowModal = false;
    },

    showEditApprovalWorkflow(approval_workflow) {
      this.approval_workflow = approval_workflow;
      this.showEditApprovalWorkflowModal = true;
    },
    confirmEditApprovalWorkflow() {
      this.showEditApprovalWorkflowModal = false;
    },
    cancelEditApprovalWorkflow() {
      this.showEditApprovalWorkflowModal = false;
    },

    showDeleteConfirmation(id) {
      this.deleteApprovalWorkflowId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },

  },
};
</script>
