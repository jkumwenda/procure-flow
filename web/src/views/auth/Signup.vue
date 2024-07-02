<template>
  <div class="flex flex-col space-4">
    <div class="flex flex-col space-y-4">
      <h1 class="flex justify-center text-4xl font-bold">Sign Up</h1>
      <p class="flex justify-center text-center">
        Enter your credentials to access your account
      </p>
      <form class="flex flex-col space-y-4">
        <label class="block">
          <span
            class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700"
          >
            Email address
          </span>
          <input
            type="email"
            name="email"
            class="mt-2 px-3 py-3 bg-white border shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
            placeholder="you@example.com"
          />
        </label>

        <label class="block">
          <span
            class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700"
          >
            Password
          </span>
          <input
            type="password"
            name="password"
            class="mt-2 px-3 py-3 bg-white border shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-2xl sm:text-sm focus:ring-1"
            placeholder="*******"
          />
        </label>
        <p class="flex justify-end">Forgot password?</p>
        <button
          type="submit"
          class="mt-2 px-3 py-3 text-catskill-white-100 bg-catalina-blue rounded-2xl"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignUpView",
};
</script>
