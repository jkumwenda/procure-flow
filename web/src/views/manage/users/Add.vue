<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Add user</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Add user</span>
    </p>
  </div>
  <SpinnerComponent v-if="isLoading" />
  <div v-else class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="addUser" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Firtsname
        </span>
        <input type="input" name="firstname" v-model="userData.firstname"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Firstname" />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Lastname
        </span>
        <input type="input" name="lastname" v-model="userData.lastname"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="Lastname" />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Email address
        </span>
        <input type="email" name="email" v-model="userData.email"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          placeholder="you@example.com" />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Phone
        </span>
        <input type="text" name="phone" v-model="userData.phone"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
          title="Please enter a valid 10-digit phone number" placeholder="Phone number" required />
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-2xl">
          Save
        </button>
        <router-link :to="{ name: 'Users' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-2xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>

import { createItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";

export default {
  name: "AddUserView",
  data() {
    return {
      userData: {
        firstname: "",
        lastname: "",
        email: "",
        phone: "",
        password: "",
        passwordConfirm: "",
        verified: 1,
      },
      isLoading: false,
    };
  },
  components: {
    SpinnerComponent,
  },
  methods: {
    async addUser() {
      this.isLoading = true;
      try {
        const response = await createItem("users", this.userData);
        this.users = response.data;
        this.isLoading = false;
        router.push("/user/" + response.user_id);
      } catch (error) {
        console.error("Error fetching users:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
