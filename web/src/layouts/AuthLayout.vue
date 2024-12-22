<template>
  <div class="flex items-center h-screen">
    <div class="flex flex-col space-y-4 h-screen w-screen">
      <div class="flex sm:flex-row flex-col bg-catskill-white-100 rounded-2xl">
        <div class="sw:w-8/12 w-screen bg-selago-600 h-screen p-10 grid place-items-center">
          <div class="flex flex-col items-center justify-center">
            <logo class="flex text-catalina-blue">
              <h1 class="text-6xl font-bold">ProcureFlow</h1>
              <h5 class="text-2xl">&trade;</h5>
            </logo>
          </div>
        </div>
        <div class="p-10 sw:w-4/12 w-screen grid items-center">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AuthLayout",
};
</script>
