<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Edit position</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Edit position</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editPosition" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Position
        </span>
        <input type="input" name="position" v-model="positionData.position"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Position amount" required />
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'Positions' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditPositionView",
  data() {
    return {
      id: this.$route.params.id,
      positionData: {
        position: "",
      },
      position: {},
      isLoading: true,
    };
  },
  mounted() {
    this.getPosition();
  },
  methods: {
    async editPosition() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "positions",
          this.id,
          this.positionData
        );
        this.position = response.data;
        this.isLoading = false;
        router.push("/positions");
      } catch (error) {
        console.error("Error fetching positions:", error);
        this.isLoading = false;
      }
    },
    async getPosition() {
      try {
        const response = await fetchItem("positions", this.id);
        this.positionData.position = response.position;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching positions:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
