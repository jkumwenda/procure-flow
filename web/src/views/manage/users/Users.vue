<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">Users</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>Users</span>
        </p>
      </div>
      <div class="flex border-b justify-between border-b-catskill-white-600 pb-4 items-center">
        <router-link v-if="permissions.includes('WRITE_USER')" :to="{ name: 'AddUser' }"
          class="text-center flex flex-row py-2 bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
          Add user
        </router-link>
        <div class=""><search-component @search="handleSearch"></search-component></div>
      </div>
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div>
          <div class="flex flex-row p-2 text-xs font-bold uppercase bg-catskill-white-500">
            <p class="w-3/12 ">Firstname</p>
            <p class="w-3/12 ">Lastname</p>
            <p class="w-4/12 ">Username</p>
            <p class="w-1/12 ">Phone</p>
            <p class="flex flex-1 justify-end">Action</p>
          </div>
          <div class="flex flex-row p-2 text-md border-b border-catskill-white-600" v-for="user in users" :key="user.id">
            <p class="w-3/12 ">{{ user.firstname }}</p>
            <p class="w-3/12 ">{{ user.lastname }}</p>
            <p class="w-4/12 ">{{ user.email }}</p>
            <p class="w-1/12 justify-start">{{ user.phone }}</p>
            <p class="flex flex-1  justify-end">
              <router-link v-if="permissions.includes('READ_USER')" :to="{ name: 'User', params: { id: user.id } }"
                class="cursor-pointer">
                <EyeIcon class="h-6 w-6 font-bold text-mountain-meadow-500"></EyeIcon>
              </router-link>
              <router-link v-if="permissions.includes('UPDATE_USER')" :to="{ name: 'EditUser', params: { id: user.id } }"
                class="cursor-pointer">
                <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
              </router-link>
              <TrashIcon v-if="permissions.includes('DELETE_USER')" @click="showDeleteConfirmation(user.id)"
                class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
            </p>
          </div>
        </div>
        <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
        </pagination-component>
      </div>
      <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteUser(deleteUserId)"
        @canceled="cancelDelete"></delete-confirmation-modal>
    </div>
  </div>
</template>
<script>
import { TrashIcon, PencilAltIcon, EyeIcon } from "@heroicons/vue/outline";
import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import SearchComponent from "@/components/Search.vue";
import PaginationComponent from "@/components/Pagination.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "UsersView",
  components: {
    TrashIcon,
    PencilAltIcon,
    EyeIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    SearchComponent,
    PaginationComponent
  },
  data() {
    return {
      users: [], // Store API data here
      isLoading: true,
      showDeleteModal: false,
      deleteUserId: null,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getUsers();
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async getUsers() {
      this.isLoading = true;
      try {
        const response = await fetchData("users", this.currentPage, this.pageSize, this.searchPhrase);
        this.users = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching users:", error);
        this.isLoading = false;
      }
    },
    async handleSearch(searchQuery) {
      this.searchPhrase = searchQuery
      this.getUsers();
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.getUsers();
    },
    async deleteUser(id) {
      this.isLoading = true;
      try {
        await deleteItem("users", id);
        const index = this.users.findIndex((user) => user.id === id);
        if (index !== -1) {
          this.users.splice(index, 1);
        }
        this.isLoading = false;
        this.showDeleteModal = false;
      } catch (error) {
        console.error("Error fetching users:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showDeleteConfirmation(id) {
      this.deleteUserId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
  },
};
</script>
