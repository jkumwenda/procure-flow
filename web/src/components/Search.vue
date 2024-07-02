<template>
    <form @submit.prevent="addRole" method="POST" class="flex flex-row space-x-4">
        <input v-model="searchQuery" placeholder="Search..."
            class="px-3 py-2 bg-white border border-1 shadow-sm border-silver-600 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block rounded-xl sm:text-sm focus:ring-1" />
        <button @click="search"
            class="flex flex-row text-center py-2 px-3 text-catskill-white-100 hover:bg-gradient-to-l hover:from-catalina-blue-400 shadow-sm hover:bg-catalina-blue-100 rounded-xl py-1 font-roboto-light bg-gradient-to-l from-catalina-blue-500 to-catalina-blue-300  rounded-xl">
            Search
        </button>
    </form>
</template>

<script>
export default {
    name: "SearchComponent",
    data() {
        return {
            searchQuery: "",
        };
    },
    methods: {
        search() {
            this.$emit("search", this.searchQuery);
        },
    },
};
</script>