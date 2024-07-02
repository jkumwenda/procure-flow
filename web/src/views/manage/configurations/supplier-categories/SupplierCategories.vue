<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">System Supplier Categories</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>Supplier categories</span>
        </p>
      </div>
      <div class="flex border-b justify-between border-b-catskill-white-600 pb-4 items-center">
        <router-link v-if="permissions.includes('ADD_SUPPLIER_CATEGORY')" :to="{ name: 'AddSupplierCategory' }"
          class="text-center flex flex-row py-2 bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
          Add supplier category
        </router-link>
        <div class=""><search-component @search="handleSearch"></search-component></div>
      </div>
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div>
          <div class="flex flex-row p-2 text-xs font-bold uppercase bg-catskill-white-500 rounded-xl">
            <p class="w-4/12">Supplier Category</p>
            <p class="w-4/12">Description</p>
            <p class="flex flex-1 justify-end">Action</p>
          </div>
          <div class="flex flex-row p-2 text-md border-b border-catskill-white-600"
            v-for="supplierCategory in supplierCategorys" :key="supplierCategory.id">
            <p class="w-4/12">{{ supplierCategory.supplier_category }}</p>
            <p class="w-4/12">{{ supplierCategory.description }}</p>
            <p class="flex flex-1 justify-end w-4/12 font-bold">
              <router-link v-if="permissions.includes('UPDATE_SUPPLIER_CATEGORY')" :to="{
                name: 'EditSupplierCategory',
                params: { id: supplierCategory.id },
              }" class="cursor-pointer">
                <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
              </router-link>
              <TrashIcon v-if="permissions.includes('DELETE_SUPPLIER_CATEGORY')"
                @click="showDeleteConfirmation(supplierCategory.id)"
                class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
            </p>
          </div>
        </div>
        <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
        </pagination-component>
      </div>
    </div>
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteSupplierCategory(deleteSupplierCategoryId)"
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
  name: "SupplierCategoriesView",
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
      supplierCategorys: {},
      isLoading: true,
      showDeleteModal: false,
      deleteSupplierCategoryId: null,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getSupplierCategories();
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async getSupplierCategories() {
      this.isLoading = true;
      try {
        const response = await fetchData("supplier_categories", this.currentPage, this.pageSize, this.searchPhrase);
        this.supplierCategorys = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching supplier categories:", error);
        this.isLoading = false;
      }
    },
    async handleSearch(searchQuery) {
      this.searchPhrase = searchQuery
      this.getSupplierCategories();
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.getSupplierCategories();
    },

    async deleteSupplierCategory(id) {
      this.isLoading = true;
      try {
        await deleteItem("supplier_categories", id);
        const index = this.supplierCategorys.findIndex(
          (supplierCategory) => supplierCategory.id === id
        );
        if (index !== -1) {
          this.supplierCategorys.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching supplier categories:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showDeleteConfirmation(id) {
      this.deleteSupplierCategoryId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
  },
};
</script>
