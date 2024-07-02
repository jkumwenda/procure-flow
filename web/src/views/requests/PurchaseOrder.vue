<template>
  <div
    class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Purchase order details</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'AddRequest' }" class="font-bold hover:text-selago-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Purchase order</span>
    </p>
  </div>
  <SpinnerComponent v-if="isLoading" />
  <div v-else class="flex flex-row space-x-4 z-10">
    <div class="flex flex-col space-y-4 w-8/12 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
      <div class="flex flex-col space-y-1 p-4 rounded-xl bg-selago-600 text-sm">
        <div class="flex flex-row ">
          <div class="w-2/12 font-bold ">Purchase order#</div>
          <div class="flex-1">:
            {{ getYear(purchaseOrder.purchase_order_date) }}0000{{ purchaseOrder.id }}
          </div>
        </div>
        <div class="flex flex-row ">
          <div class="w-2/12 font-bold ">Supplier</div>
          <div class="flex-1">:
            {{ supplier.supplier }}
          </div>
        </div>
        <div class="flex flex-row flex-1">
          <div class="w-2/12 font-bold ">Request</div>
          <div class="flex-1">:
            {{ purchaseOrder.request }}
          </div>
        </div>
        <div class="flex flex-row flex-1">
          <div class="w-2/12 font-bold ">Request by</div>
          <div class="flex-1">:
            {{ purchaseOrder.request_by }}
          </div>
        </div>
        <div class="flex flex-row flex-1">
          <div class="w-2/12 font-bold ">Date</div>
          <div class="flex-1">:
            {{ formatDate(purchaseOrder.purchase_order_date) }}
          </div>
        </div>
      </div>
      <div class="flex flex-col space-y-1">
        <div class="flex space-x-4 p-4 py-2 rounded-md bg-selago-500 text-sm font-bold">
          <div class="w-3/12">Item</div>
          <div class="w-5/12">Description</div>
          <div class="w-1/12">quantity</div>
          <div class="w-1/12">Amount</div>
          <div class="w-2/12 flex justify-end">Controls</div>
        </div>
        <div v-for="purchase_order_item in purchase_order_items" :key="purchase_order_item.id"
          class="flex space-x-4 p-4 py-2 rounded-md border border-1 border-selago-600 z-10">
          <div class="w-3/12">
            {{ purchase_order_item.item }}
          </div>
          <div class="w-5/12">
            {{ purchase_order_item.description }}
          </div>
          <div class="w-1/12">
            {{ purchase_order_item.quantity }}
          </div>
          <div class="w-1/12">
            {{ purchase_order_item.amount }}
          </div>
          <div class="flex w-2/12 flex justify-end">
            <PencilAltIcon @click="showEditPurchaseOrderItem(purchase_order_item)"
              class="h-6 w-6 font-bold text-dodger-blue-500 cursor-pointer">
            </PencilAltIcon>
            <TrashIcon @click="showDeleteConfirmation(purchase_order_item.id)"
              class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer">
            </TrashIcon>
          </div>
        </div>
      </div>
      <div v-if="purchaseOrder.purchase_order_status == 1" class="">
        <button @click="showAddPurchaseOrderItem"
          class="flex px-3 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl text-sm">
          <PlusCircleIcon class="h-5 w-5 font-bold text-catalina-100"></PlusCircleIcon>Assign items to PO
        </button>
      </div>
      <div class="flex space-x-2 pt-4 rounded-xl border-t-8 border-catalina-blue  text-sm">
        <button @click="showDownloadRequest"
          class="flex px-3 py-2 text-catskill-white-100 bg-catalina-blue-50 hover:bg-catalina-blue-200 rounded-xl text-sm">
          <PrinterIcon class="h-5 w-5 font-bold text-catalina-100"></PrinterIcon>Print
        </button>

        <template v-if="purchase_order_approval_history.length === 0 || purchaseOrder.purchase_order_status == 3">
          <button v-if="purchaseOrder.raiser_id == userId" type="submit" @click="showSubmitPurchaseOrder"
            class="flex px-3 py-2 text-catskill-white-100 bg-mountain-meadow-500 hover:bg-mountain-meadow-600 rounded-xl text-sm">
            <PaperAirplaneIcon class="h-5 w-5 font-bold text-catalina-100"></PaperAirplaneIcon>Submit
          </button>
        </template>

        <template v-else>
          <template v-for="historyItem in purchase_order_approval_history" :key="historyItem.id">
            <div v-if="historyItem.approval_status === 0">
              <div v-if="historyItem.approver_id == userId" class="flex space-x-4">
                <button type="submit" @click="showSubmitPurchaseOrder"
                  class="flex px-3 py-2 text-catskill-white-100 bg-mountain-meadow-500 hover:bg-mountain-meadow-600 rounded-xl text-sm">
                  <PaperAirplaneIcon class="h-5 w-5 font-bold text-catalina-100"></PaperAirplaneIcon>Submit
                </button>
                <button type="submit" @click="showRejectRequest"
                  class="flex px-3 py-2 text-amber-800 bg-amber-200 hover:bg-amber-300 rounded-xl text-sm">
                  <RefreshIcon class="h-5 w-5 font-bold text-catalina-100"></RefreshIcon>Return
                </button>
              </div>
            </div>
          </template>
        </template>
      </div>
    </div>
    <div class="flex flex-col space-y-4 w-4/12 flex-1 items-center bg-catskill-white-100 p-4 rounded-xl shadow-sm">
      <div class="flex flex-row space-x-1 bg-selago-600 rounded-xl p-4">
        <p class=" font-bold">Status</p>
        <p v-if="purchaseOrder.purchase_order_status == 1">: Draft</p>
        <p v-else-if="purchaseOrder.purchase_order_status == 2">: Under-review</p>
        <p v-else-if="purchaseOrder.purchase_order_status == 3">: Return for review</p>
        <p v-else-if="purchaseOrder.purchase_order_status == 4">: Approved</p>
      </div>
      <div class="font-bold text-lg">Approval history</div>
      <template v-for="     historyItem in purchase_order_approval_history     " :key="historyItem.id">
        <div v-if="historyItem.approval_status !== 4"
          class="flex flex-col text-sm space-y-1 w-full rounded-xl p-4 pb-2 border-2 border border-selago-600">
          <div class="flex">
            <div class="flex flex-col flex-1">
              <div class="flex">
                <p class="font-bold">Name</p>
                <p>: {{ historyItem.firstname }} {{ historyItem.lastname }}</p>
              </div>
              <div class="flex">
                <p class="font-bold">Date</p>
                <p>: {{ historyItem.date }}</p>
              </div>
              <div class="flex items-center">
                <p class="font-bold">Action :</p>
                <p class="p-1 px-2 mx-2 bg-catalina-blue-100 rounded-md text-catskill-white-100 text-sm"> {{
                  historyItem.approval_action }}</p>
              </div>
            </div>
            <div>
              <ClockIcon v-if="historyItem.approval_status === 0" class="w-10 h-10 text-selago-700 ">
              </ClockIcon>
              <CheckCircleIcon v-else-if="historyItem.approval_status === 1" class="w-10 h-10 text-mountain-meadow-500">
              </CheckCircleIcon>
              <ArrowCircleLeftIcon v-else-if="historyItem.approval_status === 2" class="w-10 h-10 text-flamingo-500 ">
              </ArrowCircleLeftIcon>
              <ClipboardCheckIcon v-else-if="historyItem.approval_status === 3"
                class="w-10 h-10 text-catalina-blue-50 ">
              </ClipboardCheckIcon>
            </div>
          </div>
          <div v-for="     comment in historyItem.comment     " :key="comment.id" class="flex">
            <AnnotationIcon @mouseover="showComment(comment.id, $event)" @mouseleave="showComment(null, $event)"
              class="h-6 w-6 font-bold text-catalina-blue-50"></AnnotationIcon>
            <div v-if="hoveredComment === comment.id" class="absolute bg-catskill-white-100 p-2 rounded-xl shadow-md"
              :style="{ top: `${mouseY}px`, left: `${mouseX}px`, zIndex: 9999 }">
              {{ comment.comment }}
            </div>
          </div>
        </div>
      </template>
    </div>
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deletePurchaseOrderItem(deletePurchaseOrderItemId)"
      @canceled="cancelDelete"></delete-confirmation-modal>

    <add-purchase-order-item-modal :show="showAddPurchaseOrderItemModal" @confirmed="confirmAddPurchaseOrderItem"
      @closed="cancelAddPurchaseOrderItem" :purchaseOrderId="purchaseOrder.id" :purchaseOrder="purchaseOrder"
      @item-added="refreshItems">
    </add-purchase-order-item-modal>

    <edit-purchase-order-item-modal :show="showEditPurchaseOrderItemModal" @confirmed="confirmEditPurchaseOrderItem"
      @closed="cancelEditPurchaseOrderItem" :purchase_order_id="purchaseOrder.id" :item="item"
      :purchaseOrder="purchaseOrder" @item-updated="purchaseOrderItemUpdated">
    </edit-purchase-order-item-modal>

    <submit-purchase-order-modal :show="showSubmitPurchaseOrderModal" @confirmed="confirmSubmitPurchaseOrder"
      @closed="cancelSubmitPurchaseOrder" :purchase_order_id="purchaseOrder.id" @purchase-order-submitted="refreshPage">
    </submit-purchase-order-modal>

    <reject-purchase-order-modal :show="showRejectPurchaseOrderModal" @confirmed="confirmRejectRequest"
      @closed="cancelRejectRequest" :purchase_order_id="purchaseOrder.id" @purchase-order-submitted="refreshPage">
    </reject-purchase-order-modal>

    <download-purchase-order-modal :show="showDownloadPurchaseOrderModal" :purchase_order_data="purchase_order_data"
      @downloaded="confirmDownloadRequest" :purchase_order_id="purchaseOrder.id"
      @purchase-order-submitted="refreshPage">
    </download-purchase-order-modal>

  </div>
</template>

<script>
import {
  TrashIcon,
  PencilAltIcon,
  PlusCircleIcon,
  PrinterIcon,
  RefreshIcon,
  AnnotationIcon,
  PaperAirplaneIcon,
  CheckCircleIcon, ClockIcon, ArrowCircleLeftIcon, ClipboardCheckIcon
} from "@heroicons/vue/outline";
import { fetchItem, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import AddPurchaseOrderItemModal from "@/components/AddPurchaseOrderItemModal.vue";
import EditPurchaseOrderItemModal from "@/components/EditPurchaseOrderItemModal.vue";
import SubmitPurchaseOrderModal from "@/components/SubmitPurchaseOrderModal.vue";
import RejectPurchaseOrderModal from "@/components/RejectPurchaseOrderModal.vue";
import DownloadPurchaseOrderModal from "@/components/DownloadPurchaseOrderModal.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "PurchaseOrderView",
  components: {
    PlusCircleIcon,
    TrashIcon,
    PencilAltIcon,
    PrinterIcon,
    RefreshIcon,
    AnnotationIcon,
    PaperAirplaneIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    AddPurchaseOrderItemModal,
    EditPurchaseOrderItemModal,
    SubmitPurchaseOrderModal,
    DownloadPurchaseOrderModal,
    RejectPurchaseOrderModal,
    CheckCircleIcon,
    ClockIcon,
    ArrowCircleLeftIcon,
    ClipboardCheckIcon,
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
      purchaseOrder: {},
      purchase_order_data: {},
      supplier: {},
      purchase_order_items: {},
      purchase_order_approval_history: {},
      isLoading: true,

      showDeleteModal: false,
      showAddPurchaseOrderItemModal: false,
      showEditPurchaseOrderItemModal: false,
      showUploadRequestFileModal: false,
      deletePurchaseOrderItemId: null,
      showSubmitPurchaseOrderModal: false,
      showRejectPurchaseOrderModal: false,
      showDownloadPurchaseOrderModal: false,
      item: {},
      hoveredComment: null,
      userId: "",
    };
  },

  mounted() {
    this.getPurchaseOrder();
  },
  setup() {
    const authStore = useAuthStore()
    const loginUser = authStore.loginUser
    const permissions = authStore.permissions
    return { loginUser, permissions }
  },
  methods: {
    async refreshItems() {
      await this.getPurchaseOrder();
    },
    async purchaseOrderItemUpdated() {
      await this.getPurchaseOrder();
      this.showEditPurchaseOrderItemModal = false;
    },
    async refreshPage() {
      await this.getPurchaseOrder();
      this.showSubmitPurchaseOrderModal = false;

    },
    async getPurchaseOrder() {
      this.isLoading = true;
      try {
        const response = await fetchItem("purchase_orders", this.id);
        this.purchase_order_data = response
        this.purchaseOrder = response.purchase_order;
        this.supplier = response.supplier;
        this.purchase_order_items = response.purchase_order_items;
        this.purchase_order_approval_history = response.purchase_order_approval_history;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching request:", error);
        this.isLoading = false;
      }
    },

    async deletePurchaseOrderItem(id) {
      this.isLoading = true;
      try {
        await deleteItem("purchase_orders/purchase_order_items", id);
        const index = this.purchase_order_items.findIndex((purchase_order_item) => purchase_order_item.id === id);
        if (index !== -1) {
          this.purchase_order_items.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching request_items:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },

    toggleExpand() {
      this.expanded = !this.expanded;
    },
    showDeleteConfirmation(id) {
      this.deletePurchaseOrderItemId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },

    showAddPurchaseOrderItem() {
      this.showAddPurchaseOrderItemModal = true;
    },
    confirmAddPurchaseOrderItem() {
      this.showAddPurchaseOrderItemModal = false;
    },
    cancelAddPurchaseOrderItem() {
      this.showAddPurchaseOrderItemModal = false;
    },

    showEditPurchaseOrderItem(item) {
      this.item = item;
      this.showEditPurchaseOrderItemModal = true;
    },
    confirmEditPurchaseOrderItem() {
      this.showEditPurchaseOrderItemModal = false;
    },
    cancelEditPurchaseOrderItem() {
      this.showEditPurchaseOrderItemModal = false;
    },
    showUploadRequestFile() {
      this.showUploadRequestFileModal = true;
    },
    confirmUploadRequestFile() {
      this.showUploadRequestFileModal = false;
    },
    cancelUploadRequestFile() {
      this.showUploadRequestFileModal = false;
    },

    showSubmitPurchaseOrder() {
      this.showSubmitPurchaseOrderModal = true;
    },
    confirmSubmitPurchaseOrder() {
      this.showSubmitPurchaseOrderModal = false;
    },
    cancelSubmitPurchaseOrder() {
      this.showSubmitPurchaseOrderModal = false;
    },

    showRejectRequest() {
      this.showRejectPurchaseOrderModal = true;
    },
    confirmRejectRequest() {
      this.showRejectPurchaseOrderModal = false;
    },
    cancelRejectRequest() {
      this.showRejectPurchaseOrderModal = false;
    },

    showDownloadRequest() {
      this.showDownloadPurchaseOrderModal = true;
    },
    confirmDownloadRequest() {
      this.showDownloadPurchaseOrderModal = false;
    },

    showComment(commentId) {
      this.hoveredComment = commentId;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const formattedDate = date.toLocaleString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      return formattedDate;
    },
    getYear(dateString) {
      const date = new Date(dateString);
      const formattedDate = date.toLocaleString("en-US", {
        year: "numeric",
      });
      return formattedDate;
    },
  },

};
</script>