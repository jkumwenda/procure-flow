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
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 px-4 rounded-2xl shadow-sm">
        <div class="flex flex-col">
          <p class="text-2xl font-semibold">
            {{ supplier.supplier }}
          </p>
          <p class="text-md font-semibold">
            {{ supplier.address }}
          </p>
          <p class="text-md font-semibold">
            {{ supplier.email }}
          </p>
          <p class="text-md font-semibold">
            {{ supplier.phone }}
          </p>
        </div>
        <div class="flex flex-col">
          <div class="flex flex-row space-x-2 text-sm text-dodger-blue-800 py-2 border-b border-1 border-dodger-blue-500">
            <p class="font-bold">Category of supply</p>
            <p class="capitalize">(click to remove)</p>
          </div>
          <div class="flex flex-row flex-wrap my-4">
            <button class="bg-dodger-blue-100 text-dodger-blue-800 rounded-xl px-4 py-1 m-1"
              v-for="assigned_supplier_category in assigned_supplier_categories" :key="assigned_supplier_category.id"
              @click="deleteSupplierPermission(assigned_supplier_category.id)">
              {{ assigned_supplier_category.supplier_category }}
            </button>
          </div>
          <div class="flex flex-row space-x-2 text-sm text-dodger-blue-800 py-2 border-b border-1 border-dodger-blue-500">
            <p class="font-bold">Category of supply</p>
            <p class="capitalize">(click to assign)</p>
          </div>
          <div class="flex flex-row flex-wrap my-4">
            <button class="bg-dodger-blue-200 text-dodger-blue-800 rounded-xl px-4 py-1 m-1"
              v-for="supplier_category in filteredPermissions" :key="supplier_category.id"
              @click="addSupplierPermission(supplier_category.id)">
              {{ supplier_category.supplier_category }}
            </button>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchItem, fetchData, createItem, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  name: "SupplierView",
  components: {
    SpinnerComponent,
  },
  data() {
    return {
      id: this.$route.params.id,
      isLoading: true,
      supplier: {},
      assigned_supplier_categories: [],
      supplier_categories: [],
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  computed: {
    filteredPermissions() {
      return this.supplier_categories.filter((supplier_category) => {
        const supplier_categoryId = supplier_category.id;
        return !this.assigned_supplier_categories.some(
          (assigned_supplier_category) => assigned_supplier_category.supplier_category_id === supplier_categoryId
        );
      });
    },
  },
  mounted() {
    this.getSupplier();
    this.getPermissions();
  },
  methods: {
    async getSupplier() {
      try {
        const response = await fetchItem("suppliers", this.id);
        this.supplier = response.supplier;
        this.assigned_supplier_categories = response.supplier_categories;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching suppliers:", error);
        this.isLoading = false;
      }
    },
    async getPermissions() {
      try {
        const response = await fetchData("supplier_categories", this.currentPage, this.pageSize, this.searchPhrase);
        this.supplier_categories = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching supplier_categories:", error);
        this.isLoading = false;
      }
    },

    async deleteSupplierPermission(supplier_supplier_category_id) {
      this.isLoading = true;
      try {
        await deleteItem("suppliers/supplier_categories", supplier_supplier_category_id);
        const index = this.assigned_supplier_categories.findIndex((assigned_supplier_category) => assigned_supplier_category.id === supplier_supplier_category_id);
        if (index !== -1) {
          this.assigned_supplier_categories.splice(index, 1);
        }
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching supplier_categories:", error);
        this.isLoading = false;
      }
      const index = this.assigned_supplier_categories.findIndex(
        (assigned_supplier_category) => assigned_supplier_category.id === supplier_supplier_category_id
      );
      if (index !== -1) {
        this.assigned_supplier_categories.splice(index, 1);
      }
    },


    async addSupplierPermission(supplier_categoryId) {
      const supplierPermissionData = {
        supplier_id: this.id,
        supplier_category_id: supplier_categoryId,
      };
      this.isLoading = true;
      try {
        await createItem("suppliers/supplier_categories/", supplierPermissionData);
        this.getSupplier();
        this.getPermissions();
        this.isLoading = false;
      } catch (error) {
        console.error("Error add supplier supplier_category failed:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
