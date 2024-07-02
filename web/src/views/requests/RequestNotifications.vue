<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Requests for your action</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Pending requests</span>
    </p>
  </div>
  <div class="flex border-b border-b-catskill-white-600 pb-4">
    <div>
      Click on the tab to open:
    </div>
    <div class="flex-1"></div>
  </div>
  <SpinnerComponent v-if="isLoading" />
  <div v-else class="flex flex-row flex-wrap">
    <div v-for="historyItem in historyItems" :key="historyItem.id" class="w-6/12">
      <router-link :to="{ name: 'Request', params: { id: historyItem.request_id } }" class="flex flex-col rounded-xl space-y-1 m-1 flex-1 p-4 shadow-sm bg-catskill-white-100 cursor-pointer border-t
        border-t-4 border-catalina-blue-100">
        <div class="flex flex-row flex-1 space-x-4">
          <p class="font-bold w-2/12 text-catalina-blue-400">Request title</p>:
          <p class="">{{ historyItem.request }}</p>
        </div>
        <div class="flex flex-row space-x-4">
          <p class="font-bold w-2/12 text-catalina-blue-400">Request by</p>:
          <p class="">{{ historyItem.firstname }} {{ historyItem.lastname }}</p>
        </div>
        <div class="flex flex-row space-x-4">
          <p class="font-bold w-2/12 text-catalina-blue-400">Date</p>:
          <p class="">{{ formatDate(historyItem.date) }}</p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { fetchData } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  name: "RequestNotificationsView",
  components: {
    SpinnerComponent
  },
  data() {
    return {
      id: 0,
      historyItems: [],
      count: [],
      isLoading: true,
    };
  },
  mounted() {
    this.getRequestsNotifications();
  },
  methods: {
    async getRequestsNotifications() {
      this.isLoading = true;
      try {
        const response = await fetchData("requests/notifications/");
        this.historyItems = response.notifications;
        this.count = response.total_approvals;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.isLoading = false;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const formattedDate = date.toLocaleString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      return formattedDate;
    },
  },
};
</script>
