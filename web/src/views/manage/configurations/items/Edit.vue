<template>
  <div
    class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Add item</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Add item</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editItem" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Item name
        </span>
        <input type="input" name="item" v-model="itemData.item"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Item" required />
      </label>
      <label class="block">
        <select name="role"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          v-model="itemData.unit_of_measure_id">
          <option value="" disabled selected>--Select a unit of measure--</option>
          <option v-for="unit_of_measure in unit_of_measures" :key="unit_of_measure.id" :value="unit_of_measure.id">
            {{ unit_of_measure.unit_of_measure }}
          </option>
        </select>
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'Items' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { updateItem, fetchItem, fetchData } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditItemView",
  data() {
    return {
      id: this.$route.params.id,
      itemData: {
        item: "",
        unit_of_measure_id: "",
      },
      unit_of_measures: {},
      isLoading: true,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getItem();
    this.getUnitOfMeasures();
  },
  methods: {
    async getUnitOfMeasures() {
      try {
        const response = await fetchData("unit_of_measures", this.currentPage, this.pageSize, this.searchPhrase);
        this.unit_of_measures = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching unit of measures:", error);
        this.isLoading = false;
      }
    },
    async editItem() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "items",
          this.id,
          this.itemData
        );
        this.item = response.data;
        this.isLoading = false;
        router.push("/items");
      } catch (error) {
        console.error("Error fetching items:", error);
        this.isLoading = false;
      }
    },
    async getItem() {
      try {
        const response = await fetchItem("items", this.id);
        this.itemData.item = response.item;
        this.itemData.unit_of_measure_id = response.unit_of_measure_id;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching items:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
