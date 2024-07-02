<template>
  <div class="flex flex-col space-4">
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div class="flex flex-col items-center justify-center">
        <router-link :to="{ name: 'Login' }"><img alt="Vue logo" class="w-48" src="@/assets/logo.png" /></router-link>
        <h1 class="flex text-4xl font-thin font-roboto-light">Password reset!</h1>
        <p class="pb-5">
          Provide your login email to reset password!
        </p>
      </div>
      <div v-if="message" class="text-mountain-meadow-500">{{ message }} <router-link :to="{ name: 'Login' }"
          class="text-catalina-blue-100 font-bold">Login</router-link></div>
      <div v-if="incorrectMessage" class="text-flamingo-500">{{ incorrectMessage }}</div>
      <form class="flex flex-col space-y-4" @submit.prevent="submitPasswordReset" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Email address
          </span>
          <input type="email" name="email" v-model="passwordResetData.email"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="you@example.com" required />
        </label>
        <button type="submit"
          class="mt-2 px-3 py-3 text-catskill-white-100 hover:bg-gradient-to-l hover:from-catalina-blue-400 hover:to-catalina-blue-200 bg-gradient-to-l from-catalina-blue-500 to-catalina-blue-300  rounded-xl">
          Reset password
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from "@/services/authService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  name: "ResetPasswordView",
  data() {
    return {
      passwordResetData: {
        email: "",
      },
      SpinnerComponent,
      message: null,
      incorrectMessage: null,
      isLoading: false,

    };
  },
  mounted() { },
  methods: {
    async submitPasswordReset() {
      this.isLoading = true;
      try {
        await login("auth/reset_password/", this.passwordResetData);
        this.message = "Password reset was successful, check your email!";
        this.incorrectMessage = null;
        this.isLoading = false;
      } catch (error) {
        this.incorrectMessage = "Email address does not exist in the system!";
        this.isLoading = false;
        this.message = null;
      }
    },
  },
};
</script>
