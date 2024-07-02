<!-- src/components/Dropdown.vue -->
<template>
  <div class="relative inline-block text-left">
    <button @click="isOpen = !isOpen"
      class="text-gray-700 font-semibold hover:text-gray-900 focus:outline-none focus:ring">
      {{ loginUser.firstname }}
      {{ loginUser.lastname }}
    </button>

    <div v-if="isOpen"
      class="origin-top-right absolute right-0 mt-2 w-32 rounded-md shadow-lg bg-catskill-white-100 ring-1 ring-black ring-opacity-5">
      <div class="py-2 space-y-2" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
        <a @click="profile" class="block px-4 cursor-pointer text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
          My profile
        </a>
        <a @click="logout" class="block px-4 cursor-pointer text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
          Logout
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import { useAuthStore } from "@/store/authStore";
import { logout } from "@/services/apiService";

export default {
  name: "DropdownComponent",
  props: {
    label: String,
  },
  data() {
    return {
      isOpen: false,
    };
  },
  setup() {
    const authStore = useAuthStore()
    const loginUser = authStore.loginUser
    return { loginUser }
  },
  methods: {
    async profile() { router.push("/user/" + this.loginUser.id); },

    async logout() {
      const authStore = useAuthStore();
      this.isLoading = true;
      try {
        await logout("auth/logout");
        this.isLoading = false;
        authStore.reset();
        router.push("/");
      } catch (error) {
        console.error("Error fetching request:", error);
        this.isLoading = false;
      }
    }
  }
};
</script>
