<template>
  <div
    class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Request details</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'AddRequest' }" class="font-bold hover:text-selago-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Request</span>
    </p>
  </div>
  <SpinnerComponent v-if="isLoading" />
  <div v-else class="flex flex-col space-y-4 z-10">
    <div class="flex flex-col space-y-4 w-11/12 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
      <div class="flex flex-col space-y-1 p-4 rounded-xl bg-selago-600 text-sm">
        <div class="flex flex-row ">
          <div class="w-2/12 font-bold ">Request Title</div>
          <div class="flex-1">:
            {{ request.request }}
          </div>
        </div>
        <div class="flex flex-row ">
          <div class="w-2/12 font-bold ">Requested by</div>
          <div class="flex-1">:
            {{ requester.firstname }}
            {{ requester.lastname }}
          </div>
        </div>
        <div class="flex flex-row flex-1">
          <div class="w-2/12 font-bold ">Department</div>
          <div class="flex-1">:
            {{ department.department }}
          </div>
        </div>
      </div>
      <div class="flex flex-col space-y-2">
        <div class="flex space-x-4 p-4 py-2 rounded-md bg-selago-500 text-sm font-bold">
          <div class="w-3/12">Item</div>
          <div class="w-1/12">Measure</div>
          <div class="w-6/12">Description</div>
          <div class="w-1/12">Qty</div>
          <div class="w-1/12">Controls</div>
        </div>
        <div v-for="item in items" :key="item.id"
          class="flex space-x-4 p-4 py-2 rounded-md border border-1 border-selago-600 z-10">
          <div class="w-3/12">
            {{ item.item }}
          </div>
          <div class="w-1/12">
            {{ item.unit_of_measure }}
          </div>
          <div class="w-6/12">
            {{ item.description }}
          </div>
          <div class="w-1/12">
            {{ item.quantity }}
          </div>
          <div class="w-1/12">
            <ViewBoardsIcon @click="showAddPO(item.id)"
              class="h-6 w-6 font-bold text-mountain-meadow-500 cursor-pointer"
              title="This symbolizes your being locked inside">
            </ViewBoardsIcon>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col space-y-3 w-11/12 flex-1">
      <div class="font-bold text-lg">Purchase orders for this request</div>
      <div v-if="message" class="p-3 text-sm rounded-xl text-catskill-white-100 py-2 text bg-mountain-meadow-500">{{
        message }}
      </div>
      <div v-for="purchaseOrder in purchaseOrders" :key="purchaseOrder.id"
        class="flex flex-row space-x-1 bg-catskill-white-100  rounded-xl p-3 shadow-sm">
        <div class="flex flex-1 items-center px-3">
          <div>{{ purchaseOrder.supplier }}</div>
        </div>
        <div class="flex justify-center items-center w-2/12 flex justify-end">
          <router-link :to="{ name: 'PurchaseOrder', params: { id: purchaseOrder.id } }">
            <EyeIcon class="h-6 w-6 font-bold text-mountain-meadow-500 cursor-pointer">
            </EyeIcon>
          </router-link>
          <PencilAltIcon @click="showEditPO(purchaseOrder)"
            class="h-6 w-6 font-bold text-dodger-blue-500 cursor-pointer">
          </PencilAltIcon>
          <TrashIcon @click="showDeleteConfirmation(purchaseOrder.id)"
            class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer">
          </TrashIcon>
        </div>
      </div>
    </div>
    <AddPOModal :show="showAddPOModal" @confirmed="confirmAddPO" @closed="cancelAddPO" :request_id="request.id"
      :item_id="item_id">
    </AddPOModal>

    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deletePurchaseOrder(deletePurchaseOrderId)"
      @canceled="cancelDelete">
    </delete-confirmation-modal>

    <EditPOModal :show="showEditPOModal" @confirmed="confirmEditPO" @closed="cancelEditPO" :request_id="request.id"
      :purchaseOrder="purchaseOrder">
    </EditPOModal>
  </div>
</template>
<script>
import {
  TrashIcon,
  PencilAltIcon, ViewBoardsIcon, EyeIcon
} from "@heroicons/vue/outline";
import { fetchItem, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import AddPOModal from "@/components/AddPOModal.vue";
import EditPOModal from "@/components/EditPOModal.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";

export default {
  name: "GeneratePOView",
  components: {
    SpinnerComponent,
    AddPOModal,
    EditPOModal,
    TrashIcon,
    PencilAltIcon,
    ViewBoardsIcon, EyeIcon,
    DeleteConfirmationModal
  },
  data() {
    return {
      requestData: {
        request: "",
        request_id: 0,
        item_id: "",
        description: "",
        quantity: "",
      },
      id: this.$route.params.id,
      request: {},
      request_data: {},
      department: {},
      requester: {},
      purchaseOrders: {},
      items: {},
      expanded: false,
      isLoading: true,
      showDeleteModal: false,
      showAddPOModal: false,
      showEditPOModal: false,
      userId: "",
      message: "",
      deletePurchaseOrderId: null,
      purchaseOrder: {},
      purchase_order_id: null,
      item_id: ""
    };
  },
  mounted() {
    this.getRequest();
  },
  methods: {
    async refreshItems() {
      await this.getRequest();
    },
    async refreshPage() {
      await this.getRequest();
      this.showSubmitRequestModal = false;

    },
    async getRequest() {
      this.userId = localStorage.getItem('userId');
      this.isLoading = true;
      try {
        const response = await fetchItem("requests", this.id);
        this.request_data = response
        this.request = response.request;
        this.department = response.department;
        this.requester = response.requester;
        this.items = response.items;
        this.purchaseOrders = response.purchase_orders;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching request:", error);
        this.isLoading = false;
      }
    },

    async deletePurchaseOrder(id) {
      this.isLoading = true;
      try {
        await deleteItem("purchase_orders", id);
        const index = this.purchaseOrders.findIndex((purchaseOrder) => purchaseOrder.id === id);
        if (index !== -1) {
          this.purchaseOrders.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching approval workflows:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    showAddPO(item_id) {
      this.item_id = item_id
      this.showAddPOModal = true;
    },
    confirmAddPO() {
      this.getRequest();
      this.showAddPOModal = false;
      this.message = "LPO Supplier added, add items for the supplier"
    },
    cancelAddPO() {
      this.showAddPOModal = false;
    },
    showEditPO(purchaseOrder) {
      this.purchaseOrder = purchaseOrder;
      this.showEditPOModal = true;
    },
    confirmEditPO() {
      this.getRequest();
      this.showEditPOModal = false;
      this.message = "LPO Supplier updated, add items for the supplier or submit"
    },
    cancelEditPO() {
      this.showEditPOModal = false;
    },
    showDeleteConfirmation(id) {
      this.deletePurchaseOrderId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
  },
};
</script>