<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Add financial year</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Add financial year</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="addFinancialYear" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Financial year
        </span>
        <input type="input" name="financial_year" v-model="financialYearData.financial_year"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Financial Year" required />
      </label>
      <div class="flex block space-x-4">
        <label class="block w-6/12">
          <span class="after:content-['*'] mb-2 after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Start date
          </span>
          <VueDatePicker type="date" v-model="financialYearData.start_date" name="financial_year"
            :enable-time-picker="false" :format="'yyyy-MM-dd'" placeholder="Start date" required>
          </VueDatePicker>
        </label>
        <label class="block w-6/12">
          <span class="after:content-['*'] mb-2 after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            End date
          </span>
          <VueDatePicker type="date" v-model="financialYearData.end_date" name="financial_year"
            :enable-time-picker="false" :format="'yyyy-MM-dd'" placeholder="End date" required>
          </VueDatePicker>
        </label>
      </div>
      <label class="flex flex-col space-y-2 block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Is current budget
        </span>
        <div class="flex">
          <div class="flex items-center mr-4">
            <input checked id="inline-checked-radio" type="radio" value="true" v-model="financialYearData.status"
              name="inline-radio-group"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
            <label for="inline-radio" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Yes</label>
          </div>
          <div class="flex items-center mr-4">
            <input id="inline-2-radio" type="radio" value="" name="inline-radio-group" v-model="financialYearData.status"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
            <label for="inline-2-radio" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">No</label>
          </div>
        </div>
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'FinancialYears' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { createItem } from "@/services/apiService";
import router from "@/router";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

export default {
  name: "AddFinancialYearView",
  components: { VueDatePicker },
  data() {
    return {
      financialYearData: {
        financial_year: "",
        start_date: new Date(),
        end_date: new Date(),
        status: true,
      },
      isLoading: true,
    };
  },
  methods: {
    formatDateForSubmit() {
      const formattedStartDate = this.financialYearData.start_date.toISOString().split('T')[0];
      const formattedEndDate = this.financialYearData.start_date.toISOString().split('T')[0];
      this.financialYearData.start_date = formattedStartDate;
      this.financialYearData.end_date = formattedEndDate;
    },

    async addFinancialYear() {
      this.isLoading = true;
      try {
        const response = await createItem(
          "financial_years",
          this.financialYearData
        );
        this.financialYears = response.data;
        this.isLoading = false;
        router.push("/financial-years");
      } catch (error) {
        console.error("Error fetching financial years:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
