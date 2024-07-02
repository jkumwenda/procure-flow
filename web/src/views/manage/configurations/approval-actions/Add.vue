<template>
  <div
    class="flex flex-col space-y-1 font-roboto-light rounded-xl text-catskill-white-50 bg-catalina-blue-500 px-4 py-2">
    <p class="font-bold text-md">Add approval action</p>
    <p class="text-sm font-roboto-light text-catskill-white-800">
      <router-link :to="{ name: 'Dashboard' }" class="font-bold hover:text-catskill-white-600">Dashboard</router-link>
      <span class="px-2">|</span>
      <span>Add approval action</span>
    </p>
  </div>
  <div class="flex flex-1 bg-catskill-white-100 p-4 rounded-xl shadow-sm">
    <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="addApprovalAction" method="POST">
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Approval action
        </span>
        <input type="input" name="approval_action" v-model="approvalActionData.approval_action"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="approval action" required />
      </label>
      <label class="block">
        <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
          Description
        </span>
        <textarea type="textarea" name="description" v-model="approvalActionData.description"
          class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
          placeholder="Description" required></textarea>
      </label>
      <div class="flex flex-row space-x-4">
        <button type="submit"
          class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
          Save
        </button>
        <router-link :to="{ name: 'ApprovalActions' }"
          class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
<script>
import { createItem } from "@/services/apiService";
import router from "@/router";

export default {
  name: "AddApprovalActionView",
  data() {
    return {
      approvalActionData: {
        approval_action: "",
        description: "",
      },
      isLoading: true,
    };
  },
  methods: {
    async addApprovalAction() {
      this.isLoading = true;
      try {
        const response = await createItem(
          "approval_actions",
          this.approvalActionData
        );
        this.ApprovalActions = response.data;
        this.isLoading = false;
        router.push("/approval-actions");
      } catch (error) {
        console.error("Error fetching file approval actions:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
