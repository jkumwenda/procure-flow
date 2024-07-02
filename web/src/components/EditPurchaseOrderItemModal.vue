<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div
      class="flex flex-col border-2 border-catalina-blue-500 border-t-8 bg-catskill-white-100 dark:bg-gray-800 rounded-xl shadow-lg w-5/12 z-50">
      <div class="border-b font-bold text-lg border-b-4 p-4 px-6 space-y-4 border-b-silver-500">
        Purchase order item details
      </div>
      <div v-if="message" class="p-4 m-6 rounded-xl text-catskill-white-100 py-2 text bg-mountain-meadow-500">{{
        message }}
      </div>
      <form class="flex flex-col space-y-4 p-4 px-6 space-y-4" @submit.prevent="editPurchaseOrderItem" method="POST">
        <SpinnerComponent v-if="isLoading" />
        <label v-else class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Request item
          </span>
          <select name="role" required
            class="mt-3 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="purchaseOrderItemData.request_item_id">
            <option value="" disabled selected>--Select item--</option>
            <option v-for="item in items" :key="item.id" :value="item.id">
              {{ item.item }}
            </option>
          </select>
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Amount
          </span>
          <input type="number" name="amount" v-model="purchaseOrderItemData.amount"
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
import { fetchItem, updateItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  components: {
    SpinnerComponent
  },
  data() {
    return {
      purchaseOrderItemData: {
        purchase_order_id: "",
        request_item_id: "",
        amount: "",
      },
      items: {},
      request_item: "",
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
    purchaseOrderId: {
      type: Number,
      required: true,
    },
    item: {
      type: Object,
      required: true,
    },
    purchaseOrder: {
      type: Object,
      required: true,
    },
  },
  watch: {
    item: {
      immediate: true,
      handler(newItem) {
        if (newItem) {
          this.loadData(newItem);
        }
      },
    },
  },

  mounted() {
    this.RequestItems();
  },

  methods: {
    async RequestItems() {
      this.requestId = this.purchaseOrder.request_id
      try {
        const response = await fetchItem("requests", this.requestId);
        this.items = response.items;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching items:", error);
        this.isLoading = false;
      }
    },

    loadData(newItem) {
      this.purchaseOrderItemData = {
        purchase_order_id: newItem.purchase_order_id,
        request_item_id: newItem.request_item_id,
        amount: newItem.amount,
      };
    },

    async editPurchaseOrderItem() {
      this.isLoading = true; close
      console.log("Request is good", this.purchaseOrderItemData);
      try {
        const response = await updateItem("purchase_orders/purchase_order_items", this.item.id, this.purchaseOrderItemData);
        this.request_item = response.data;
        this.isLoading = false;
        this.message = "Purchase order item updated successfully"
        this.$emit("item-updated");
        // this.$emit("confirmed");
      } catch (error) {
        console.error("Error fetching request item:", error);
        this.isLoading = false;
      }
    },
    close() {
      this.$emit("closed");
    },
  },
};
</script>
