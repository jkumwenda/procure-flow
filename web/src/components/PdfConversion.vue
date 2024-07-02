<template>
    <div>
        <h1 class="text-2xl font-semibold mb-4">HTML Table to PDF Conversion</h1>

        <!-- Your HTML table to be converted -->
        <table id="myTable" class="table-auto">
            <thead>
                <tr>
                    <th class="border">Name</th>
                    <th class="border">Age</th>
                    <th class="border">Country</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="border"></td>
                    <td class="border">30</td>
                    <td class="border">USA</td>
                </tr>
                <tr>
                    <td class="border">Jane Smith</td>
                    <td class="border">25</td>
                    <td class="border">Canada</td>
                </tr>
            </tbody>
        </table>

        <button @click="convertToPDF" class="bg-blue-500 text-white px-4 py-2 mt-4 rounded">Convert to PDF</button>
    </div>
</template>

<script>
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default {
    methods: {
        convertToPDF() {
            const doc = new jsPDF();

            // Define the HTML table element to be converted
            const table = document.getElementById('myTable');

            // Create an Image object for the logo
            const img = new Image();
            img.src = require('@/assets/logo.png'); // Adjust the path as needed

            // Ensure the image is loaded before generating the PDF
            img.onload = () => {
                // Add the logo to the PDF
                doc.addImage(img, 'PNG', 10, 10, 50, 50); // Adjust coordinates and dimensions

                // Extract table data and add it to the PDF
                doc.autoTable({ html: table });

                // Save the PDF
                doc.save('table_with_logo.pdf');
            };
        },
    }
};
</script>

<style scoped>
.table {
    width: 100%;
    border-collapse: collapse;
}

.table th,
.table td {
    border: 1px solid #e2e8f0;
    padding: 0.5rem;
}
</style>
