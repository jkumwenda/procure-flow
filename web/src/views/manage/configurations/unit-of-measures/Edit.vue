<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Edit unit of measure</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Edit unit of measure</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editUnitOfMeasure" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Unit of measure
        </span>
        <input type="input" name="unit_of_measure" v-model="unitOfMeasureData.unit_of_measure"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Unit of measure" required />
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'UnitOfMeasures' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditUnitOfMeasureView",
  components: {

  },
  data() {
    return {
      id: this.$route.params.id,
      unitOfMeasureData: {
        unit_of_measure: "",
      },
      isLoading: true,
    };
  },
  mounted() {
    this.getUnitOfMeasure();
  },
  methods: {
    async editUnitOfMeasure() {
      this.isLoading = true;
      try {
        const response = await updateItem("unit_of_measures", this.id, this.unitOfMeasureData);
        this.unit_of_measure = response.data;
        this.isLoading = false;
        router.push("/unit-of-measures");
      } catch (error) {
        console.error("Error fetching unit of measures:", error);
        this.isLoading = false;
      }
    },
    async getUnitOfMeasure() {
      try {
        const response = await fetchItem("unit_of_measures", this.id);
        console.log("JOEL KUMWENDA")
        this.unitOfMeasureData.unit_of_measure = response.unit_of_measure;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching unit of measure:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
