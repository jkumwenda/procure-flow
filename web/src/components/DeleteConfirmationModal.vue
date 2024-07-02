<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div
      class="flex flex-col justify-center items-center border border-catskill-white-500 border-t-2 bg-catskill-white-100 dark:bg-gray-800 rounded-2xl shadow-lg p-4 w-96 z-50">
      <p class="text-lg font-light mb-4">
        <XCircleIcon class="h-12 w-12 text-flamingo-500" />
      </p>
      <p class="text-2xl font-semibold mb-4">Are you sure?</p>
      <p class="mb-4">{{ message }}</p>
      <div class="flex justify-end">
        <button @click="cancel"
          class="bg-dodger-blue-500 hover:bg-blue-600 text-catskill-white-100 py-2 px-4 rounded-2xl mr-2">
          Cancel
        </button>
        <button @click="confirm" class="bg-flamingo-500 hover:bg-red-600 text-catskill-white-100 py-2 px-4 rounded-2xl">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { XCircleIcon } from "@heroicons/vue/outline";

export default {
  components: {
    XCircleIcon,
  },
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    message: {
      type: String,
      default: "Are you sure you want to delete this item?",
    },
  },
  methods: {
    confirm() {
      this.$emit("confirmed");
    },
    cancel() {
      this.$emit("canceled");
    },
  },
};
</script>
