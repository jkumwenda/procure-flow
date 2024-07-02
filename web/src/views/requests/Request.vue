<template>
  <div class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Request details</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'AddRequest' }" class="font-bold hover:text-selago-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Request</span>
    </p>
  </div>
  <SpinnerComponent v-if="isLoading" />
  <div v-else class="flex flex-row space-x-4 z-10">
    <div class="flex flex-col space-y-4 w-8/12 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
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
        <div class="flex flex-row flex-1">
          <div class="w-2/12 font-bold ">Date</div>
          <div class="flex-1">:
            {{ request.request_date }}
          </div>
        </div>
      </div>
      <div class="flex-col space-y-2">
        <div
          class="flex space-x-2 p-4 py-2 border-2 border border-selago-600 rounded-xl text-amber-800 text-sm font-bold cursor-pointer"
          @click="toggleExpand">
          Uploads (Click to expand)
          <i :class="{ 'rotate-90': expanded, 'transition-transform duration-300 ease-in-out': true }"
            class="fas fa-chevron-right"></i>
        </div>
        <transition name="fade-slide w-8/12">
          <div v-if="expanded" key="content" class="p-4 py-3 bg-amber-50 rounded-xl">
            <div class="border-b border-1 border-b border-b-amber-400 mb-2 pb-2">
              <div v-for="file in files" :key="file.id"
                class="flex flex-row space-x-4 p-1 px-4 border rounded-md block mb-1 bg-catskill-white-300">
                <div class="w-8/12">{{ file.file_name }}</div>
                <div class="flex-1">{{ fileExtension(file.real_file_name) }}</div>
                <div class="flex items-end">
                  <DocumentDownloadIcon class="w-6 h-6 cursor-pointer text-dodger-blue-500"
                    @click="downloadRequestFile(file.id, accessToken)">
                  </DocumentDownloadIcon>
                </div>
              </div>
            </div>
            <button @click="showUploadRequestFile()"
              class="flex px-3 py-1 text-amber-700 border border-2 border-amber-600 hover:bg-amber-200 rounded-md text-sm font-bold">
              <UploadIcon class="h-5 w-5 font-bold text-catalina-100"></UploadIcon> Upload file
            </button>
          </div>
        </transition>
      </div>
      <div class="flex flex-col space-y-1">
        <div class="flex space-x-4 p-4 py-2 rounded-md bg-selago-500 text-sm font-bold">
          <div class="w-3/12">Item</div>
          <div class="w-1/12">Measure</div>
          <div class="w-5/12">Description</div>
          <div class="w-1/12">Quantity</div>
          <div class="w-2/12 flex justify-end">Controls</div>
        </div>
        <div v-for="item in items" :key="item.id"
          class="flex space-x-4 p-4 py-2 rounded-md border border-1 border-selago-600 z-10">
          <div class="w-3/12">
            {{ item.item }}
          </div>
          <div class="w-1/12">
            {{ item.unit_of_measure }}
          </div>
          <div class="w-5/12">
            {{ item.description }}
          </div>
          <div class="w-1/12">
            {{ item.quantity }}
          </div>
          <div class="flex w-2/12 flex justify-end">
            <PencilAltIcon @click="showEditRequestItem(item)"
              class="h-6 w-6 font-bold text-dodger-blue-500 cursor-pointer">
            </PencilAltIcon>
            <TrashIcon @click="showDeleteConfirmation(item.id)"
              class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer">
            </TrashIcon>
          </div>
        </div>
      </div>
      <div v-if="request.request_status == 1" class="">
        <button @click="showAddRequestItem"
          class="flex px-3 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl text-sm">
          <PlusCircleIcon class="h-5 w-5 font-bold text-catalina-100"></PlusCircleIcon>Add item
        </button>

      </div>
      <div class="flex space-x-2 pt-4 rounded-xl border-t-8 border-catalina-blue  text-sm">
        <button @click="showDownloadRequest"
          class="flex px-3 py-2 text-catskill-white-100 bg-catalina-blue-50 hover:bg-catalina-blue-200 rounded-xl text-sm">
          <PrinterIcon class="h-5 w-5 font-bold text-catalina-100"></PrinterIcon>Print
        </button>

        <template v-if="request_approval_history.length === 0 || request.request_status == 3">
          <button v-if="request.requester_id == loginUser.id" type="submit" @click="showSubmitRequest"
            class="flex px-3 py-2 text-catskill-white-100 bg-mountain-meadow-500 hover:bg-mountain-meadow-600 rounded-xl text-sm">
            <PaperAirplaneIcon class="h-5 w-5 font-bold text-catalina-100"></PaperAirplaneIcon>Submit
          </button>
        </template>

        <template v-else>
          <template v-for="historyItem in request_approval_history" :key="historyItem.id">
            <div v-if="historyItem.approval_status === 0">
              <div v-if="historyItem.approver_id == loginUser.id" class="flex space-x-4">
                <button type="submit" @click="showSubmitRequest"
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
        <p v-if="request.request_status == 1">: Draft</p>
        <p v-else-if="request.request_status == 2">: Under-review</p>
        <p v-else-if="request.request_status == 3">: Return for review</p>
        <p v-else-if="request.request_status == 4">: Approved</p>
      </div>
      <div class="font-bold text-lg">Approval history</div>
      <template v-for="     historyItem      in      request_approval_history     " :key="historyItem.id">
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
              <ClipboardCheckIcon v-else-if="historyItem.approval_status === 3" class="w-10 h-10 text-catalina-blue-50 ">
              </ClipboardCheckIcon>
            </div>
          </div>
          <div v-for="     comment      in      historyItem.comment     " :key="comment.id" class="flex">
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
    <!-- Add the DeleteConfirmationModal component -->
    <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteRequestItem(deleteRequestItemId)"
      @canceled="cancelDelete"></delete-confirmation-modal>

    <add-request-item-modal :show="showAddRequestItemModal" @confirmed="confirmAddRequestItem"
      @closed="cancelAddRequestItem" :request_id="request.id" @item-added="refreshItems">
    </add-request-item-modal>

    <edit-request-item-modal :show="showEditRequestItemModal" @confirmed="confirmEditRequestItem"
      @closed="cancelEditRequestItem" :request_id="request.id" :item="item" @item-added="refreshItems">
    </edit-request-item-modal>

    <upload-request-file-modal :show="showUploadRequestFileModal" @confirmed="confirmUploadRequestFile"
      @closed="cancelUploadRequestFile" :request_id="request.id" @file-uploaded="refreshItems">
    </upload-request-file-modal>

    <submit-request-modal :show="showSubmitRequestModal" @confirmed="confirmSubmitRequest" @closed="cancelSubmitRequest"
      :request_id="request.id" @request-submitted="refreshPage">
    </submit-request-modal>

    <reject-request-modal :show="showRejectRequestModal" @confirmed="confirmRejectRequest" @closed="cancelRejectRequest"
      :request_id="request.id" @request-submitted="refreshPage">
    </reject-request-modal>

    <download-request-modal :show="showDownloadRequestModal" :request_data="request_data"
      @downloaded="confirmDownloadRequest" :request_id="request.id" @request-submitted="refreshPage">
    </download-request-modal>

  </div>
</template>

<script>
import {
  TrashIcon,
  PencilAltIcon,
  PlusCircleIcon,
  PrinterIcon,
  RefreshIcon,
  UploadIcon,
  AnnotationIcon,
  PaperAirplaneIcon,
  DocumentDownloadIcon, CheckCircleIcon, ClockIcon, ArrowCircleLeftIcon, ClipboardCheckIcon
} from "@heroicons/vue/outline";
import { fetchItem, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import AddRequestItemModal from "@/components/AddRequestItemModal.vue";
import EditRequestItemModal from "@/components/EditRequestItemModal.vue";
import UploadRequestFileModal from "@/components/UploadRequestFileModal.vue";
import SubmitRequestModal from "@/components/SubmitRequestModal.vue";
import RejectRequestModal from "@/components/RejectRequestModal.vue";
import DownloadRequestModal from "@/components/DownloadRequestModal.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "RequestView",
  components: {
    PlusCircleIcon,
    TrashIcon,
    PencilAltIcon,
    PrinterIcon,
    RefreshIcon,
    UploadIcon,
    AnnotationIcon,
    PaperAirplaneIcon,
    DocumentDownloadIcon,
    SpinnerComponent,
    DeleteConfirmationModal,
    AddRequestItemModal,
    EditRequestItemModal,
    UploadRequestFileModal,
    SubmitRequestModal,
    DownloadRequestModal,
    RejectRequestModal,
    CheckCircleIcon,
    ClockIcon,
    ArrowCircleLeftIcon,
    ClipboardCheckIcon
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
      items: {},
      files: {},
      request_approval_history: {},
      api_url: "",
      expanded: false,
      isLoading: true,
      showDeleteModal: false,
      showAddRequestItemModal: false,
      showEditRequestItemModal: false,
      showUploadRequestFileModal: false,
      deleteRequestItemId: null,
      showSubmitRequestModal: false,
      showRejectRequestModal: false,
      showDownloadRequestModal: false,
      item: {},
      hoveredComment: null,
    };
  },
  setup() {
    const authStore = useAuthStore()
    const loginUser = authStore.loginUser
    const permissions = authStore.permissions
    const accessToken = authStore.accessToken
    return { loginUser, permissions, accessToken }
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
      this.isLoading = true;
      try {
        const response = await fetchItem("requests", this.id);
        this.request_data = response
        this.request = response.request;
        this.department = response.department;
        this.requester = response.requester;
        this.items = response.items;
        this.files = response.files;
        this.request_approval_history = response.request_approval_history;
        this.api_url = response.api_url
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching request:", error);
        this.isLoading = false;
      }
    },

    async deleteRequestItem(id) {
      this.isLoading = true;
      try {
        await deleteItem("requests/request_items", id);
        const index = this.items.findIndex((item) => item.id === id);
        if (index !== -1) {
          this.items.splice(index, 1);
        }
        this.showDeleteModal = false;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching request_items:", error);
        this.isLoading = false;
        this.showDeleteModal = false;
      }
    },
    downloadRequestFile(id) {
      const downloadUrl = `${this.api_url}/requests/download_request_file/${id}`; // Replace with your FastAPI endpoint URL
      window.location.href = downloadUrl;
    },
    fileExtension(file_name) {
      const parts = file_name.split('.');
      if (parts.length > 1) {
        return parts[parts.length - 1];
      } else {
        return "No extension";
      }
    },
    toggleExpand() {
      this.expanded = !this.expanded;
    },
    showDeleteConfirmation(id) {
      this.deleteRequestItemId = id;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
    },
    showAddRequestItem() {
      this.showAddRequestItemModal = true;
    },
    confirmAddRequestItem() {
      this.showAddRequestItemModal = false;
    },
    cancelAddRequestItem() {
      this.showAddRequestItemModal = false;
    },
    showEditRequestItem(item) {
      this.item = item;
      this.showEditRequestItemModal = true;
    },
    confirmEditRequestItem() {
      this.showEditRequestItemModal = false;
    },
    cancelEditRequestItem() {
      this.showEditRequestItemModal = false;
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
    showSubmitRequest() {
      this.showSubmitRequestModal = true;
    },
    confirmSubmitRequest() {
      this.showSubmitRequestModal = false;
    },
    cancelSubmitRequest() {
      this.showSubmitRequestModal = false;
    },
    showRejectRequest() {
      this.showRejectRequestModal = true;
    },
    confirmRejectRequest() {
      this.showRejectRequestModal = false;
    },
    cancelRejectRequest() {
      this.showRejectRequestModal = false;
    },
    showDownloadRequest() {
      this.showDownloadRequestModal = true;
    },
    confirmDownloadRequest() {
      this.showDownloadRequestModal = false;
    },
    confirmRequestSubmitted() {
      this.getRequest();
      this.showDownloadRequestModal = false;
    },


    showComment(commentId) {
      this.hoveredComment = commentId;
    },
  },
};
</script>