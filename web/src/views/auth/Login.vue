<template>
  <div class="flex flex-col space-4">
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div class="flex flex-col items-center justify-center">
        <router-link :to="{ name: 'Login' }"><img alt="Vue logo" class="w-48" src="@/assets/logo.png" /></router-link>
        <h1 class="flex text-4xl font-thin font-roboto-light">Welcome!</h1>
        <p class="pb-5">
          Please login to your account.
        </p>
      </div>
      <div v-if="message" class="text-red-500">{{ message }}</div> <!-- Display error message -->
      <form class="flex flex-col space-y-4" @submit.prevent="submitLoginForm" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Email address
          </span>
          <input type="email" name="username" v-model="userData.username"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="you@example.com" required />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Password
          </span>
          <input type="password" name="password" v-model="userData.password"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="********" required />
        </label>
        <router-link :to="{ name: 'ResetPassword' }" class="flex text-catalina-blue-100 justify-end">Forgot
          password?</router-link>
        <button type="submit"
          class="mt-2 px-3 py-3 text-catskill-white-100 hover:bg-gradient-to-l hover:from-catalina-blue-400 hover:to-catalina-blue-200 bg-gradient-to-l from-catalina-blue-500 to-catalina-blue-300  rounded-xl">
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from "@/services/authService";
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";
import { useAuthStore } from "@/store/authStore";
import { setAuthToken } from "@/services/apiService"; // Adjust the path as needed


export default {
  name: "LoginView",
  data() {
    return {
      userData: {
        username: "",
        password: "",
      },
      SpinnerComponent,
      message: null,
      isLoading: false,
    };
  },

  methods: {
    async submitLoginForm() {
      this.isLoading = true;
      try {
        const response = await login("auth/login", this.userData);
        // saveTokenToLocalStorage(response.access_token);
        const authStore = useAuthStore();
        authStore.setUser(response.user);
        authStore.setPermissions(response.permissions);
        authStore.setAccessToken(response.access_token);
        setAuthToken();

        this.isLoading = false;

        this.$nextTick(() => {
          router.push("/dashboard");
        });
      } catch (error) {
        this.message = "Invalid username or password!"; // Set the error message
        this.isLoading = false;
      }
    },
  },
};
</script>
