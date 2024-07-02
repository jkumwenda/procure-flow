<template>
    <div class="p-1">
        <div
            class="flex flex-col rounded-xl shadow-sm bg-catskill-white-100 border border-catskill-white-500 cursor-pointer">
            <div class="relative flex justify-end items-end">
                <div class="flex bg-catalina-blue-100 rounded-sm rounded-tr-xl rounded-bl-md py-1 text-sm font-roboto-light"
                    @click="toggleDropdown">
                    <DotsVerticalIcon class="h-5 w-5 stroke-1 text-catskill-white-100" />
                </div>
                <!-- Dropdown content -->
                <div v-if="isDropdownOpen"
                    class="p-2 py-1 absolute right-0 top-full mt-1 bg-catskill-white-500 shadow-lg rounded-md">
                    <router-link :to="{ name: 'Request', params: { id: request.request.id } }"
                        v-tooltip="'View User Details'">
                        <EyeIcon class="h-6 w-6 font-bold text-mountain-meadow-500"></EyeIcon>
                    </router-link>
                    <router-link :to="{ name: 'EditUser', params: { id: request.request.id } }" class="cursor-pointer">
                        <PencilAltIcon class="h-6 w-6 font-bold text-dodger-blue-500"></PencilAltIcon>
                    </router-link>
                    <TrashIcon @click="showDeleteConfirmation(request.request.id)"
                        class="h-6 w-6 font-bold text-flamingo-500 cursor-pointer"></TrashIcon>
                </div>
            </div>

            <div class="pb-4 px-4">{{ request.request.request }}</div>
            <div class="border-t border-t-1 border-t-silver-300 py-2 px-4">
                <div class="flex space-x-2 items-center text-sm block font-roboto-light">
                    <CalendarIcon class="h-5 w-5 stroke-1 text-catalina-blue-200" />
                    <p>{{ formatDate(request.request.request_date) }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { TrashIcon, PencilAltIcon, EyeIcon, CalendarIcon, DotsVerticalIcon } from "@heroicons/vue/outline";

export default {
    components: {
        TrashIcon,
        PencilAltIcon,
        EyeIcon, CalendarIcon,
        DotsVerticalIcon,
    },
    props: {
        request: Object,
    },
    data() {
        return {
            isDropdownOpen: false,
        };
    },
    methods: {
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
        toggleDropdown() {
            this.isDropdownOpen = !this.isDropdownOpen;
        },
    },
};
</script>
