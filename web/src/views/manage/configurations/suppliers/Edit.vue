<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Edit supplier</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Edit supplier</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editSupplier" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Supplier
        </span>
        <input type="input" name="supplier" v-model="supplierData.supplier"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Supplier" required />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Address
        </span>
        <textarea type="textarea" name="address" v-model="supplierData.address"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Address" required></textarea>
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Email
        </span>
        <input type="input" name="email" v-model="supplierData.email"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="email@email.com" required />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Phone
        </span>
        <input type="input" name="phone" v-model="supplierData.phone"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="099999999" required />
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'Suppliers' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditSupplierView",
  data() {
    return {
      id: this.$route.params.id,
      supplierData: {
        supplier: "",
        address: "",
        email: "",
        phone: ""
      },
      supplier: {},
      isLoading: true,
    };
  },
  mounted() {
    this.getSupplier();
  },
  methods: {
    async editSupplier() {
      this.isLoading = true;
      try {
        const response = await updateItem("suppliers", this.id, this.supplierData);
        this.supplier = response.data;
        this.isLoading = false;
        router.push("/suppliers");
      } catch (error) {
        console.error("Error fetching suppliers:", error);
        this.isLoading = false;
      }
    },
    async getSupplier() {
      try {
        const response = await fetchItem("suppliers", this.id);
        this.supplierData.supplier = response.supplier.supplier;
        this.supplierData.address = response.supplier.address;
        this.supplierData.email = response.supplier.email;
        this.supplierData.phone = response.supplier.phone;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching suppliers:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
