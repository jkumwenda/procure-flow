<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Edit request</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'AddRequest' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Edit request</span>
    </p>
  </div>
  <div class="flex flex-col space-y-4 flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">

    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editRequest" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Request title
        </span>
        <input type="input" name="request" v-model="requestData.request"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Request" required />
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save and continue
        </button>
        <router-link :to="{ name: 'Requests' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { updateItem, fetchItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "EditRequestView",
  components: {

  },
  data() {
    return {
      id: this.$route.params.id,
      requestData: {
        request: "",
      },
      isLoading: true,
    };
  },
  mounted() {
    this.getRequest();
  },
  methods: {
    async editRequest() {
      this.isLoading = true;
      try {
        const response = await updateItem("requests", this.id, this.requestData);
        this.request = response.data;
        this.isLoading = false;
        router.push("/requests");
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
      }
    },
    async getRequest() {
      try {
        const response = await fetchItem("requests", this.id);
        this.requestData.request = response.request.request;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
