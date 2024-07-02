<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div
      class="flex flex-col border-2 border-catalina-blue-500 border-t-8 bg-catskill-white-100 dark:bg-gray-800 rounded-xl shadow-lg w-5/12 z-50">
      <div class="border-b font-bold text-lg border-b-4 p-4 px-6 space-y-4 border-b-silver-500">
        Request comment
      </div>
      <div v-if="message" class="p-4 m-6 rounded-xl text-catskill-white-100 py-2 text bg-mountain-meadow-500">{{
        message }}
      </div>
      <SpinnerComponent v-if="isLoading" />
      <form v-else class="flex flex-col block space-y-2 p-4 " @submit.prevent="AddSubmitRequest" method="POST">
        <label class="block">
          <textarea type="text" rows="6" name="comment" v-model="submitRequestData.comment"
            class="mt-2 px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Comment"></textarea>
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Submit request
          </button>
          <button @click="close" class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Close</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { createItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  components: {
    SpinnerComponent
  },
  data() {
    return {
      submitRequestData: {
        comment: "",
        request_id: "",
      },
      isLoading: false,
      message: "",
      submit_request: "",
    };
  },

  props: {
    show: {
      type: Boolean,
      required: true,
    },
    request_id: {
      type: Number,
      required: true,
    },
  },

  mounted() { },

  methods: {
    async AddSubmitRequest() {
      this.isLoading = true; close
      this.submitRequestData.request_id = this.request_id
      try {
        const response = await createItem("requests/request_approval_history/", this.submitRequestData);
        this.submit_request = response;
        this.isLoading = false;
        this.message = "Request submit request successfully"
        this.$emit("request-submitted");
      } catch (error) {
        console.error("Error fetching submiiting request:", error);
        this.isLoading = false;
      }
    },
    close() {
      this.$emit("closed");
    },
  },
};
</script>
