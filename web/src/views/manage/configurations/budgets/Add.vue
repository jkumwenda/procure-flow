<template>
  <div
    class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Add budget</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Add budget</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="addBudget" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Budget amount
        </span>
        <input type="input" name="budget" v-model="budgetData.amount"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Budget amount" required />
      </label>
      <label class="block">
        <select name="role"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          v-model="budgetData.department_id">
          <option value="" disabled selected>--Select a department--</option>
          <option v-for="department in departments" :key="department.id" :value="department.id">
            {{ department.department }}
          </option>
        </select>
      </label>
      <label class="block">
        <select name="role"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          v-model="budgetData.financial_year_id">
          <option value="" disabled selected>--Select financial year--</option>
          <option v-for="financial_year in financial_years" :key="financial_year.id" :value="financial_year.id">
            {{ financial_year.financial_year }}
          </option>
        </select>
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'Budgets' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { createItem, fetchData } from "@/services/apiService";
import router from "@/router";

export default {
  name: "AddBudgetView",
  data() {
    return {
      budgetData: {
        amount: "",
        department_id: "",
        financial_year_id: "",
      },
      isLoading: true,
      financial_years: {},
      departments: {},
      currentPage: 1,
      totalPages: "",
      pageSize: 100,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getFinancialYears();
    this.getDepartments();
  },
  methods: {
    async getFinancialYears() {
      try {
        const response = await fetchData("financial_years", this.currentPage, this.pageSize, this.searchPhrase);
        this.financial_years = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching finacial years:", error);
        this.isLoading = false;
      }
    },
    async getDepartments() {
      try {
        const response = await fetchData("departments", this.currentPage, this.pageSize, this.searchPhrase);
        this.departments = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching departments:", error);
        this.isLoading = false;
      }
    },
    async addBudget() {
      this.isLoading = true;
      try {
        const response = await createItem(
          "budgets",
          this.budgetData
        );
        this.Budgets = response.data;
        this.isLoading = false;
        router.push("/budgets");
      } catch (error) {
        console.error("Error fetching budgets:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
