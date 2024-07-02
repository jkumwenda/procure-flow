<template>
    <div>
        <input v-model="searchQuery" placeholder="Search..." />
        <button @click="search">Search</button>
        <ul>
            <li v-for="role in roles" :key="role.id">
                <p>{{ role.role }}</p>
                <p>{{ role.description }}</p>
            </li>
        </ul>
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <button @click="nextPage" :disabled="currentPage >= totalPages">Next</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            roles: [],
            currentPage: 1,
            pageSize: 10,
            totalPages: 1,
            searchQuery: "",
        };
    },
    methods: {
        async fetchData() {
            // Make a GET request to your FastAPI endpoint with pagination and search parameters
            const response = await fetch(`/api/roles/?skip=${(this.currentPage - 1) * this.pageSize}&limit=${this.pageSize}&search=${this.searchQuery}`);
            const data = await response.json();

            this.roles = data.data;
            this.totalPages = data.pages;
        },
        search() {
            this.currentPage = 1;
            this.fetchData();
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.fetchData();
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.fetchData();
            }
        },
    },
    mounted() {
        this.fetchData();
    },
};
</script>
