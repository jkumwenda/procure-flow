<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">Requests</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }"
            class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>Requests</span>
        </p>
      </div>
      <div class="flex border-b justify-between border-b-catskill-white-600 pb-4 items-center">
        <router-link :to="{ name: 'AddRequest' }"
          class="text-center flex flex-row py-2 bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
          Add request
        </router-link>
        <div class=""><search-component @search="handleSearch"></search-component></div>
      </div>

      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div>
          <div class="flex flex-row p-2 text-xs font-bold uppercase bg-catskill-white-500 rounded-xl">
            <p class="w-3/12">Request</p>
            <p class="w-3/12">Requested by</p>
            <p class="w-2/12">Department</p>
            <p class="w-1/12">Status</p>
            <p class="w-2/12">Date</p>
            <p class="flex flex-1 w-2/12 justify-end">Action</p>
          </div>
          <div class="flex flex-row p-2 text-md border-b border-catskill-white-600" v-for="request in requests"
            :key="request.request.id">
            <p class="w-3/12">{{ request.request.request }}</p>
            <p class="w-3/12">{{ request.requester.firstname }} {{ request.requester.lastname }}</p>
            <p class="w-2/12">{{ request.department.department }}</p>
            <p class="w-1/12">
              <span v-if="request.request.request_status === 1">Draft</span>
              <span v-else-if="request.request.request_status === 2">Under-review</span>
              <span v-else-if="request.request.request_status === 3">Return for review</span>
              <span v-else-if="request.request.request_status === 4">Approved</span>
              <span v-else-if="request.request.request_status === 5">Rejected</span>
              <span v-else>Status uknown</span>
            </p>
            <p class="w-2/12">{{ formatDate(request.request.request_date) }}</p>
            <p class="flex flex-1 w-2/12 justify-end font-bold">
              <router-link :to="{ name: 'GeneratePO', params: { id: request.request.id } }" class="cursor-pointer">
                <DocumentDuplicateIcon class="h-6 w-6 font-bold text-mountain-meadow-500"></DocumentDuplicateIcon>
              </router-link>
              <router-link :to="{ name: 'Request', params: { id: request.request.id } }" class="cursor-pointer">
                <EyeIcon class="h-6 w-6 font-bold text-mountain-meadow-500"></EyeIcon>
              </router-link>
              <router-link :to="{ name: 'EditRequest', params: { id: request.request.id } }" class="cursor-pointer">
                <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
              </router-link>
              <TrashIcon @click="showDeleteConfirmation(request.request.id)"
                class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
            </p>
          </div>
        </div>
        <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
        </pagination-component>
      </div>
    </div>
    <!-- Add the DeleteConfirmationModal component -->
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteRequest(deleteRequestId)"
      @canceled="cancelDelete"></delete-confirmation-modal>
  </div>
</template>
<script>
import { EyeIcon, TrashIcon, PencilAltIcon, DocumentDuplicateIcon } from "@heroicons/vue/outline";
import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import SearchComponent from "@/components/Search.vue";
import PaginationComponent from "@/components/Pagination.vue";

export default {
  name: "RequestsView",
  components: {
    EyeIcon,
    TrashIcon,
    PencilAltIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    SearchComponent,
    PaginationComponent,
    DocumentDuplicateIcon
  },
  data() {
    return {
      requests: {},
      isLoading: true,
      showDeleteModal: false,
      deleteRequestId: null,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getRequests();
  },
  methods: {
    async getRequests() {
      try {
        const response = await fetchData("requests", this.currentPage, this.pageSize, this.searchPhrase);
        this.requests = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
      }
    },
    async handleSearch(searchQuery) {
      this.searchPhrase = searchQuery
      this.getRequests();
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.getRequests();
    },
    async deleteRequest(id) {
      this.isLoading = true;
      try {
        await deleteItem("requests", id);
        const index = this.requests.findIndex((request) => request.request.id === id);
        if (index !== -1) {
          this.requests.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showDeleteConfirmation(id) {
      this.deleteRequestId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const formattedDate = date.toLocaleString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      });
      return formattedDate;
    },
  },
};
</script>
