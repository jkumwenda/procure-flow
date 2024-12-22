<template>
    <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
        <div
            class="flex flex-col border-2 border-catalina-blue-500 border-t-8 bg-catskill-white-100 dark:bg-gray-800 rounded-xl shadow-lg w-5/12 z-50">
            <div class="font-bold text-lg border-b-4 p-4 px-6 space-y-4 border-b-silver-500">
                New password
            </div>
            <div v-if="message"
                class="p-4 m-6 m-y-4 rounded-xl py-2 text bg-mountain-meadow-100 text-mountain-meadow-700">
                {{ message }}
            </div>
            <form class="flex flex-col p-4 px-6 space-y-4" @submit.prevent="updatePassword" method="POST">
                <SpinnerComponent v-if="isLoading" />
                <label class="block">
                    <span
                        class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
                        New password
                    </span>
                    <input type="text" v-model="passwordData.password"
                        class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                        placeholder="New password" required />
                </label>
                <div class="flex flex-row space-x-4">
                    <button type="submit"
                        class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
                        Save
                    </button>
                    <button @click="close"
                        class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Close</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { updateItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
    components: {
        SpinnerComponent
    },
    data() {
        return {
            passwordData: {
                password: "",
            },
            isLoading: false,
            message: "",
        };
    },


    props: {
        show: {
            type: Boolean,
            required: true,
        },
        user_id: {
            type: Number,
            required: true,
        },
    },

    methods: {

        async updatePassword() {
            this.isLoading = true;
            try {
                const response = await updateItem("users/reset_password", this.user_id, this.passwordData
                );
                this.user_data = response.data;
                this.isLoading = false;
                this.$emit("password-set");
                this.message = "Password updated successfully";
            } catch (error) {
                this.isLoading = false;
            }
        },
        close() {
            this.$emit("closed");
        },
    },
};
</script>
