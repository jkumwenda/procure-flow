<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">My Requests</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Procurement</span>
    </p>
  </div>
  <div class="flex border-b border-b-catskill-white-600 pb-4">
    <router-link :to="{ name: 'AddRequest' }"
      class="items-center flex flex-row bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
      New Request
    </router-link>
    <div class="flex-1"></div>
  </div>
  <SpinnerComponent v-if="isLoading" />
  <div v-else class="flex space-x-4">
    <div class="flex flex-col space-y-4 w-3/12">
      <div class="flex space-x-2 items-center">
        <div class="p-4 bg-catskill-white-700 rounded-full"></div>
        <h1 class="flex-1 font-bold">Draft</h1>
      </div>
      <div class="p-1">
        <template v-if="hasRequests(1)">
          <request-item-card v-for="request in filteredRequests(1)" :key="request.id" :request="request" />
        </template>
        <template v-else>
          <div class="p-1justify-center items-center text-center">
            <div
              class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
              <div class="pl-2">No requests in draft</div>
            </div>
          </div>
        </template>
      </div>
    </div>
    <div class="flex flex-col space-y-4 w-3/12">
      <div class="flex space-x-2 items-center">
        <div class="p-4 bg-yellow-600 rounded-full"></div>
        <h1 class="flex-1 font-bold">Under-review</h1>
      </div>
      <div class="p-1">
        <template v-if="hasRequests(2)">
          <request-item-card v-for="request in filteredRequests(2)" :key="request.id" :request="request" />
        </template>
        <template v-else>
          <div class="p-1justify-center items-center text-center">
            <div
              class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
              <div class="pl-2">No requests under-review</div>
            </div>
          </div>
        </template>
      </div>
    </div>
    <div class="flex flex-col space-y-4 w-3/12">
      <div class="flex space-x-2 items-center">
        <div class="p-4 bg-chateau-green-500 rounded-full"></div>
        <h1 class="flex-1 font-bold">Approved</h1>
      </div>
      <div class="p-1">
        <template v-if="hasRequests(4)">
          <request-item-card v-for="request in filteredRequests(4)" :key="request.id" :request="request" />
        </template>
        <template v-else>
          <div class="p-1justify-center items-center text-center">
            <div
              class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
              <div class="pl-2">No approved requests </div>
            </div>
          </div>
        </template>
      </div>
    </div>
    <div class="flex flex-col space-y-4 w-3/12">
      <div class="flex space-x-2 items-center">
        <div class="p-4 bg-red-500 rounded-full"></div>
        <h1 class="flex-1 font-bold">Rejected</h1>
      </div>
      <div class="p-1">
        <template v-if="hasRequests(3)">
          <request-item-card v-for="request in filteredRequests(3)" :key="request.id" :request="request" />
        </template>
        <template v-else>
          <div class="p-1justify-center items-center text-center">
            <div
              class="flex flex-row items-center p-4 rounded-2xl shadow-sm bg-catskill-white-100 border border-catskill-white-100 cursor-pointer">
              <div class="pl-2">No rejected requests</div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchItem } from "@/services/apiService";
import RequestItemCard from "@/components/RequestItemCard.vue";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  name: "MyRequestsView",
  components: {
    RequestItemCard,
    SpinnerComponent
  },
  data() {
    return {
      id: 0,
      requests: [],
      isLoading: true,
    };
  },
  mounted() {
    this.getMyRequests();
  },
  methods: {
    async getMyRequests() {
      try {
        const response = await fetchItem("requests/requester", this.id);
        this.requests = response;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
      }
    },
    hasRequests(status) {
      return this.requests.some((request) => request.request.request_status === status);
    },
    filteredRequests(status) {
      return this.requests.filter((request) => request.request.request_status === status);
    },
  },
};
</script>
