<template>
  <div class="flex sm:flex-row flex-col flex-1 space-x-4">
    <SpinnerComponent v-if="isLoading" />
    <template v-else>
      <!-- <div>{{ authStore.accessToken }}</div> -->
      <div class="sm:w-8/12 w-12/12 flex flex-col space-y-4">
        <div
          class="flex sm:flex-row flex-col sm:space-x-4 sm:space-y-0 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
          <div
            class="flex-1 p-4 space-y-4 rounded-xl bg-gradient-to-l font-roboto-light from-electric-violet-500 to-electric-violet-300 text-catskill-white-100">
            <div class="flex flex-1 flex-row justify-between">
              <div class="p-2 rounded-xl items-end justify-end bg-catskill-white-100 text-electric-violet-800">
                <EyeIcon class="w-6 h-6" />
              </div>
              <icon>{{ total_users }} Users</icon>
            </div>
            <div class="flex flex-col">
              <p class="font-bold text-lg">{{ total_requests }}</p>
              <div class="flex flex-1 flex-row justify-between">
                <p class="text-sm">Total requests</p>
                <InformationCircleIcon class="w-5 h-5" />
              </div>
            </div>
          </div>
          <div
            class="flex-1 p-4 space-y-4 rounded-xl bg-gradient-to-l font-roboto-light from-flamingo-500 to-flamingo-300 text-catskill-white-100">
            <div class="flex flex-1 flex-row justify-between">
              <div class="p-2 rounded-xl items-end justify-end bg-catskill-white-100 text-flamingo-500">
                <CashIcon class="w-6 h-6" />
              </div>
              <!-- <icon>72.01%</icon> -->
            </div>
            <div class="flex flex-col">
              <p class="font-bold text-lg">MWK {{ total_budget }}</p>
              <div class="flex flex-1 flex-row justify-between">
                <p class="text-sm">Total Expenditure</p>
                <InformationCircleIcon class="w-5 h-5" />
              </div>
            </div>
          </div>
          <div
            class="flex-1 p-4 space-y-4 rounded-xl font-roboto-light bg-gradient-to-l  from-blue-ribbon-500 to-blue-ribbon-300 text-catskill-white-100">
            <div class="flex flex-1 flex-row justify-between">
              <div class="p-2 rounded-xl items-end justify-end bg-catskill-white-100 text-blue-ribbon-500">
                <ShoppingBagIcon class="w-6 h-6" />
              </div>
              <!-- <icon>93.2% --</icon> -->
            </div>
            <div class="flex flex-col">
              <p class="font-bold text-lg">{{ total_suppliers }}</p>
              <div class="flex flex-1 flex-row justify-between">
                <p class="text-sm">Number of Suppliers</p>
                <InformationCircleIcon class="w-5 h-5" />
              </div>
            </div>
          </div>
        </div>
        <div
          class="flex sm:flex-row flex-col items-center flex-1 space-x-4 justify-between bg-catskill-white-100 p-4 rounded-xl shadow-sm">
          <div class="sm:w-7/12 w-12/12">
            <BarChart />
          </div>
          <div class="sm:w-5/12 w-12/12">
            <DoughnutChart :totalBudget="total_budget" />
          </div>
        </div>
      </div>
      <div class="sm:w-4/12 w-12/12 flex flex-col space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div
          class="flex flex-col rounded-xl space-y-2 bg-catalina-blue-500 text-selago-500 p-4 items-center text-center">

          <div class="flex flex-col items-center text-center">
            <img alt="Vue logo" class="object-cover w-7/12 rounded-full" src="@/assets/profile.jpg" />
          </div>
          <div class="flex flex-col space-y-1">
            <p class="text-md font-semibold">
              {{ loginUser.firstname }} {{ loginUser.lastname }}
            </p>
            <p v-for="position in positions" :key="position.id" class="text-sm">{{ position.position }}</p>
            <div class="flex flex-row space-x-8 justify-between">
              <div
                class="flex flex-col text-center text-sm border border-2 border-catalina-blue-400 p-1 px-4 rounded-xl">
                <div class="font-bold">{{ user.user_total_requests }}</div>
                <div class="font-roboto-light">Requests</div>
              </div>
              <div
                class="flex flex-col text-center text-sm border border-2 border-catalina-blue-400 p-1 px-4 rounded-xl">
                <div class="font-bold">{{ user.approved_requests }}</div>
                <div class="font-roboto-light">Approved</div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col space-y-2">
          <h1 class="text-xl font-bold">Recent activities</h1>
          <div v-for="request in requests" :key="request.id">
            <div class="text-sm bg-catskill-white-500 p-2 rounded-xl">
              <div class="flex flex-row space-x-1">
                <p class="font-bold">Request: </p>
                <p>{{ request.request }}</p>
              </div>
              <div class="flex flex-row space-x-1">
                <p class="font-bold">Date: </p>
                <p>{{ formatDate(request.date) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import {
  EyeIcon,
  InformationCircleIcon,
  CashIcon,
  ShoppingBagIcon
} from "@heroicons/vue/outline";
import BarChart from '@/components/BarChart.vue';
import DoughnutChart from '@/components/DoughnutChart.vue';
import { fetchData } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "DashboardView",
  components: {
    EyeIcon,
    InformationCircleIcon,
    CashIcon,
    ShoppingBagIcon,
    BarChart,
    DoughnutChart,
    SpinnerComponent,
  },
  data() {
    return {
      user: {},
      positions: {},
      requests: {},
      user_total_requests: "",
      total_suppliers: "",
      total_users: "",
      total_budget: "",
      isLoading: true,
    };
  },
  setup() {
    const authStore = useAuthStore()
    const loginUser = authStore.loginUser
    return { loginUser }
  },
  mounted() {
    this.getDashboardData();
  },
  methods: {
    async refreshItems() {
      await this.getRequest();
    },
    async refreshPage() {
      await this.getRequest();
      this.showSubmitRequestModal = false;

    },
    async getDashboardData() {
      this.isLoading = true;
      try {
        const response = await fetchData("dashboard", this.id);
        this.user = response.user;
        this.positions = response.positions;
        this.requests = response.requests;
        this.total_requests = response.total_requests
        this.total_budget = response.total_budget
        this.total_users = response.total_users
        this.total_suppliers = response.total_suppliers
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching request:", error);
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
  }
};
</script>