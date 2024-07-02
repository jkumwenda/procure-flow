<template>
    <div class="flex flex-row space-x-4 text-center items-center">
        <button @click="prevPage" :disabled="currentPage === 1"
            class="p-1 px-4 rounded-xl bg-catalina-blue-500 text-catskill-white-100 cursor-pointer">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>

        <button @click="nextPage" :disabled="currentPage === totalPages"
            class="p-1 px-4 rounded-xl bg-catalina-blue-500 text-catskill-white-100 cursor-pointer">Next</button>
    </div>
</template>

<script>
export default {
    name: "PaginationComponent",
    props: {
        currentPage: Number,
        totalPages: Number,
    },
    methods: {
        prevPage() {
            console.log('Here')
            if (this.currentPage > 1) {
                this.$emit("page-change", this.currentPage - 1);
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.$emit("page-change", this.currentPage + 1);
            }
        },
    },
};
</script>