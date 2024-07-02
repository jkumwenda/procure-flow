<template>
    <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
        <div
            class="flex flex-col justify-center items-center border border-catskill-white-500 border-t-2 bg-catskill-white-100 dark:bg-gray-800 rounded-2xl shadow-lg p-4 w-96 z-50">
            <div @click="downloadPDF">
                <img alt="Download pdf" class="w-20 p-2 rounded-xl bg-catskill-white-100" src="@/assets/pdf.png" />
            </div>
        </div>
    </div>
</template>

<script>
import jsPDF from "jspdf";
import "jspdf-autotable";

export default {
    data() {
        return {
            request: {},
            department: {},
            requester: {},
            items: {},
            files: {},
            request_approval_history: {},
            api_url: "",
        };
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
        request_data: {
            type: Array,
            required: true,
        },
    },
    methods: {
        async downloadPDF() {
            const doc = this.createPDFDocument();
            const logoPath = require("@/assets/logo.png");
            const logoWidth = 50;
            const logoHeight = 30;
            doc.addImage(logoPath, "PNG", 0.5, 0.5, logoWidth, logoHeight);

            this.displayTopText(doc);
            this.requestItemsTable(doc);
            this.approvalHistoryTable(doc);
            this.savePDF(doc);
        },
        createPDFDocument() {
            return new jsPDF({
                orientation: "portrait",
                unit: "in",
                format: "letter",
            });
        },
        displayTopText(doc) {
            const { request, department, requester } = this.request_data;
            const topText = `Request: ${request.request}\nRequested: ${requester.firstname} ${requester.lastname}\nDepartment: ${department.department}\nStatus: ${this.getRequestStatus(request.request_status)}`;
            doc.setFontSize(12).text(topText, 0.5, 0.5);
        },
        requestItemsTable(doc) {
            const { items } = this.request_data;
            const tableData1 = [
                ["Item", "Measure", "Description", "Quantity"],
                ...items.map((item) => [item.item, item.unit_of_measure, item.description, item.quantity]),
            ];
            const yPos1 = 2;
            doc.setFontSize(16).text("Request Items", 0.5, yPos1); // Left-align the title
            doc.autoTable({
                head: [tableData1[0]],
                body: tableData1.slice(1),
                startY: yPos1 + 0.3, // Start the table below the title
            });
        },
        approvalHistoryTable(doc) {
            const { request_approval_history } = this.request_data;
            const filteredHistory = request_approval_history.filter((historyItem) => historyItem.approval_status > 0);
            const tableData2 = [
                ["Name", "Date", "Action"],
                ...filteredHistory.map((historyItem) => [
                    `${historyItem.firstname} ${historyItem.lastname}`,
                    historyItem.date,
                    this.getApprovalStatus(historyItem.approval_status),
                ]),
            ];
            const yPos2 = doc.autoTable.previous.finalY + 1; // Adjust the Y position
            doc.setFontSize(16).text("Approval history", 0.5, yPos2); // Left-align the title
            doc.autoTable({
                head: [tableData2[0]],
                body: tableData2.slice(1),
                startY: yPos2 + 0.3, // Start the table below the title
            });
        },
        getApprovalStatus(approvalStatus) {
            switch (approvalStatus) {
                case 1:
                    return "Draft";
                case 2:
                    return "Under-review";
                case 3:
                    return "Returned for review";
                case 4:
                    return "Approved";
                default:
                    return "Unknown";
            }
        },
        getRequestStatus(approvalStatus) {
            switch (approvalStatus) {
                case 0:
                    return "Draft";
                case 1:
                    return "Under-review";
                case 2:
                    return "Returned for review";
                case 3:
                    return "Approved";
                default:
                    return "Unknown";
            }
        },
        calculateCenterXPosition(doc, text) {
            const tableWidth = 7;
            const textWidth = doc.getTextWidth(text);
            return (tableWidth - textWidth) / 2;
        },
        savePDF(doc) {
            doc.save("request_data.pdf");
            this.$emit("downloaded");
        },
    },
};
</script>
