<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">Suppliers</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>Suppliers</span>
        </p>
      </div>
      <div class="flex border-b justify-between border-b-catskill-white-600 pb-4 items-center">
        <router-link v-if="permissions.includes('ADD_SUPPLIER')" :to="{ name: 'AddSupplier' }"
          class="text-center flex flex-row py-2 bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
          Add supplier
        </router-link>
        <div class=""><search-component @search="handleSearch"></search-component></div>
      </div>
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div>
          <div class="flex flex-row p-2 text-xs font-bold uppercase bg-catskill-white-500 rounded-xl">
            <p class="w-4/12">Supplier</p>
            <p class="w-4/12">Email</p>
            <p class="w-4/12">Phone</p>
            <p class="flex flex-1 w-4/12 justify-end">Action</p>
          </div>
          <div class="flex flex-row p-2 text-md border-b border-catskill-white-600" v-for="supplier in suppliers"
            :key="supplier.id">
            <p class="w-4/12">{{ supplier.supplier }}</p>
            <p class="w-4/12">{{ supplier.email }}</p>
            <p class="w-4/12">{{ supplier.phone }}</p>
            <p class="flex flex-1 w-4/12 justify-end font-bold">
              <router-link v-if="permissions.includes('VIEW_SUPPLIER')"
                :to="{ name: 'Supplier', params: { id: supplier.id } }" class="cursor-pointer">
                <EyeIcon class="h-6 w-6 foEyeIconnt-bold text-mountain-meadow-500"></EyeIcon>
              </router-link>
              <router-link v-if="permissions.includes('UPDATE_SUPPLIER')"
                :to="{ name: 'EditSupplier', params: { id: supplier.id } }" class="cursor-pointer">
                <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
              </router-link>
              <TrashIcon v-if="permissions.includes('DELETE_SUPPLIER')" @click="showDeleteConfirmation(supplier.id)"
                class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
            </p>
          </div>
        </div>
        <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
        </pagination-component>
      </div>
    </div>
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteSupplier(deleteSupplierId)"
      @canceled="cancelDelete">
    </delete-confirmation-modal>
  </div>
</template>
<script>
import { EyeIcon, TrashIcon, PencilAltIcon } from "@heroicons/vue/outline";
import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import SearchComponent from "@/components/Search.vue";
import PaginationComponent from "@/components/Pagination.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "SuppliersView",
  components: {
    EyeIcon,
    TrashIcon,
    PencilAltIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    SearchComponent,
    PaginationComponent
  },
  data() {
    return {
      suppliers: {},
      isLoading: true,
      showDeleteModal: false,
      deleteSupplierId: null,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getSuppliers();
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async getSuppliers() {
      this.isLoading = true;
      try {
        const response = await fetchData("suppliers", this.currentPage, this.pageSize, this.searchPhrase);
        this.suppliers = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching suppliers:", error);
        this.isLoading = false;
      }
    },

    async handleSearch(searchQuery) {
      this.searchPhrase = searchQuery
      this.getSuppliers();
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.getSuppliers();
    },

    async deleteSupplier(id) {
      this.isLoading = true;
      try {
        await deleteItem("suppliers", id);
        const index = this.suppliers.findIndex((supplier) => supplier.id === id);
        if (index !== -1) {
          this.suppliers.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching suppliers:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showDeleteConfirmation(id) {
      this.deleteSupplierId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
  },
};
</script>
