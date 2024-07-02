<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div
      class="flex flex-col border-2 border-catalina-blue-500 border-t-8 bg-catskill-white-100 dark:bg-gray-800 rounded-xl shadow-lg w-5/12 z-50">
      <div class="border-b font-bold text-lg border-b-4 p-4 px-6 space-y-4 border-b-silver-500">
        Purchase order supplier
      </div>
      <div v-if="message" class="p-4 m-6 rounded-xl text-catskill-white-100 py-2 text bg-mountain-meadow-500">{{
        message }}
      </div>
      <SpinnerComponent v-if="isLoading" />
      <form v-else class="flex flex-col space-y-4 p-4 px-6 space-y-4" @submit.prevent="addPurchaseOrder" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Supplier
          </span>
          <select name="role" required
            class="mt-3 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="requestSupplierData.supplier_id">
            <option value="" disabled selected>--Select supplier--</option>
            <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
              {{ supplier.supplier }}
            </option>
          </select>
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Amount
          </span>
          <input type="number" name="amount" v-model="requestSupplierData.amount"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Amount" required />
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Save
          </button>
          <button @click="close" class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Close</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchData, createItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  components: {
    SpinnerComponent
  },
  data() {
    return {
      requestSupplierData: {
        request_id: this.request_id,
        supplier_id: "",
        item_id: "",
        amount: "",
      },
      suppliers: {},
      purchase_order: "",
      isLoading: true,
      message: "",
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },

  props: {
    show: {
      type: Boolean,
      required: true,
    },
    request_id: {
      type: Number,
      required: true,
    },
    item_id: {
      type: Number,
      required: true,
    },
  },

  mounted() {
    this.getSuppliers();
  },

  methods: {
    async getSuppliers() {
      try {
        const response = await fetchData("suppliers", this.currentPage, this.pageSize, this.searchPhrase);
        this.suppliers = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching suppliers:", error);
        this.isLoading = false;
      }
    },
    async addPurchaseOrder() {
      this.isLoading = true; close
      this.requestSupplierData.item_id = this.item_id
      console.log("Request is good", this.requestSupplierData);
      try {
        const response = await createItem("purchase_orders/", this.requestSupplierData);
        this.purchase_order = response.data;
        this.isLoading = false;
        this.message = "Purchase orders added successfully"
        this.$emit("confirmed");
      } catch (error) {
        console.error("Error fetching purchase orders:", error);
        this.isLoading = false;
      }
    },
    close() {
      this.$emit("closed");
    },
  },
};
</script>
