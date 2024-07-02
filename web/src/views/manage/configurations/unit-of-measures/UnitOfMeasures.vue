<template>
  <div>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="flex flex-col space-y-4">
      <div
        class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
        <p class="font-bold text-md">Unit Of Measures</p>
        <p class="text-sm font-roboto-light text-catskill-white-800">
          <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
          <span class="px-2">|</span>
          <span>UnitOfMeasures</span>
        </p>
      </div>
      <div class="flex border-b justify-between border-b-catskill-white-600 pb-4 items-center">
        <router-link v-if="permissions.includes('ADD_UNIT_OF_MEASURE')" :to="{ name: 'AddUnitOfMeasure' }"
          class="text-center flex flex-row py-2 bg-catalina-blue-50 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 px-3 text-catskill-white-100 font-roboto-light">
          Add unit of measure
        </router-link>
        <div class=""><search-component @search="handleSearch"></search-component></div>
      </div>
      <div class="flex flex-col flex-1 space-y-4 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
        <div>
          <div class="flex flex-row p-2 text-xs font-bold uppercase bg-catskill-white-500 rounded-xl">
            <p class="w-4/12">Unit Of Measure</p>
            <p class="flex flex-1 justify-end">Action</p>
          </div>
          <div class="flex flex-row p-2 text-md border-b border-catskill-white-600"
            v-for="unit_of_measure in unit_of_measures" :key="unit_of_measure.id">
            <p class="w-4/12">{{ unit_of_measure.unit_of_measure }}</p>
            <p class="flex flex-1 justify-end w-4/12 font-bold">
              <router-link v-if="permissions.includes('UPDATE_UNIT_OF_MEASURE')" :to="{
                name: 'EditUnitOfMeasure',
                params: { id: unit_of_measure.id },
              }" class="cursor-pointer">
                <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
              </router-link>
              <TrashIcon v-if="permissions.includes('DELETE_UNIT_OF_MEASURE')"
                @click="showDeleteConfirmation(unit_of_measure.id)"
                class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
            </p>
          </div>
        </div>
        <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
        </pagination-component>
      </div>
    </div>
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteUnitOfMeasure(deleteUnitOfMeasureId)"
      @canceled="cancelDelete"></delete-confirmation-modal>
  </div>
</template>
<script>
import { TrashIcon, PencilAltIcon } from "@heroicons/vue/outline";
import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import SearchComponent from "@/components/Search.vue";
import PaginationComponent from "@/components/Pagination.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "UnitOfMeasuresView",
  components: {
    TrashIcon,
    PencilAltIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    SearchComponent,
    PaginationComponent
  },
  data() {
    return {
      unit_of_measures: {},
      isLoading: true,
      showDeleteModal: false,
      deleteUnitOfMeasureId: null,
      currentPage: 1,
      totalPages: "",
      pageSize: process.env.VUE_APP_PAGE_SIZE,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getUnitOfMeasures();
  },
  setup() {
    const authStore = useAuthStore()
    const permissions = authStore.permissions
    return { permissions }
  },
  methods: {
    async getUnitOfMeasures() {
      try {
        const response = await fetchData("unit_of_measures", this.currentPage, this.pageSize, this.searchPhrase);
        this.unit_of_measures = response.data;
        this.totalPages = response.pages;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching unit_of_measures:", error);
        this.isLoading = false;
      }
    },

    async handleSearch(searchQuery) {
      this.searchPhrase = searchQuery
      this.getUnitOfMeasures();
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.getUnitOfMeasures();
    },


    async deleteUnitOfMeasure(id) {
      this.isLoading = true;
      try {
        await deleteItem("unit_of_measures", id);
        const index = this.unit_of_measures.findIndex(
          (department) => department.id === id
        );
        if (index !== -1) {
          this.unit_of_measures.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching personnel cadres:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showDeleteConfirmation(id) {
      this.deleteUnitOfMeasureId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
  },
};
</script>
