<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">System Approval Actions</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>Approval actions</span>
        </p>
      </div>
      <div class="flex border-b justify-between border-b-catskill-white-600 pb-4 items-center">
        <router-link v-if="permissions.includes('ADD_APPROVAL_ACTION')" :to="{ name: 'AddApprovalAction' }"
          class="text-center flex flex-row py-2 bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
          Add approval action
        </router-link>
        <div class=""><search-component @search="handleSearch"></search-component></div>
      </div>
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div>
          <div class="flex flex-row p-2 text-xs font-bold uppercase bg-catskill-white-500 rounded-xl">
            <p class="w-4/12">Approval Action</p>
            <p class="w-4/12">Description</p>
            <p class="flex flex-1 justify-end">Action</p>
          </div>
          <div class="flex flex-row p-2 text-md border-b border-catskill-white-600"
            v-for="approvalAction in approvalActions" :key="approvalAction.id">
            <p class="w-4/12">{{ approvalAction.approval_action }}</p>
            <p class="w-4/12">{{ approvalAction.description }}</p>
            <p class="flex flex-1 justify-end w-4/12 font-bold">
              <router-link v-if="permissions.includes('UPDATE_APPROVAL_ACTION')" :to="{
                name: 'EditApprovalAction',
                params: { id: approvalAction.id },
              }" class="cursor-pointer">
                <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
              </router-link>
              <TrashIcon v-if="permissions.includes('DELETE_APPROVAL_ACTION')"
                @click="showDeleteConfirmation(approvalAction.id)"
                class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
            </p>
          </div>
        </div>
        <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
        </pagination-component>
      </div>
    </div>
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteApprovalAction(deleteApprovalActionId)"
      @canceled="cancelDelete">
    </delete-confirmation-modal>
  </div>
</template>
<script>
import { TrashIcon, PencilAltIcon } from "@heroicons/vue/outline";
import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import SearchComponent from "@/components/Search.vue";
import PaginationComponent from "@/components/Pagination.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "ApprovalActionsView",
  components: {
    TrashIcon,
    PencilAltIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    SearchComponent,
    PaginationComponent
  },
  data() {
    return {
      approvalActions: {},
      isLoading: true,
      showDeleteModal: false,
      deleteApprovalActionId: null,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getApprovalActions();
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async getApprovalActions() {
      this.isLoading = true;
      try {
        const response = await fetchData("approval_actions", this.currentPage, this.pageSize, this.searchPhrase);
        this.approvalActions = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching approval actions:", error);
        this.isLoading = false;
      }
    },
    async handleSearch(searchQuery) {
      this.searchPhrase = searchQuery
      this.getApprovalActions();
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.getApprovalActions();
    },

    async deleteApprovalAction(id) {
      this.isLoading = true;
      try {
        await deleteItem("approval_actions", id);
        const index = this.approvalActions.findIndex(
          (approvalAction) => approvalAction.id === id
        );
        if (index !== -1) {
          this.approvalActions.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching approval actions:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showDeleteConfirmation(id) {
      this.deleteApprovalActionId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
  },
};
</script>
