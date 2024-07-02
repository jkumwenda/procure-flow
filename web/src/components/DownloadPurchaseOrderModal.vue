<template>
    <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
        <div
            class="flex flex-col justify-center items-center border border-catskill-white-500 border-t-2 bg-catskill-white-100 dark:bg-gray-800 rounded-2xl shadow-lg p-2 w-36 z-50">
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
            purchase_order: {},
            supplier: {},
            purchase_order_items: {},
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
        purchase_order_data: {
            type: Array,
            required: true,
        },
    },

    methods: {
        async downloadPDF() {
            const doc = this.createPDFDocument();

            this.displayHeader(doc);
            this.requestItemsTable(doc);
            this.addSignatureSpace(doc, 177.8);
            this.savePDF(doc);
        },
        createPDFDocument() {
            return new jsPDF({
                orientation: "portrait",
                unit: "mm",
                format: "letter",
            });
        },
        displayHeader(doc) {
            const { purchase_order, supplier } = this.purchase_order_data;
            const logoPath = require("@/assets/logo.png");
            const logoWidth = 44;
            const logoHeight = 38;

            const img = new Image();
            img.src = logoPath;
            doc.addImage(logoPath, "PNG", 12.7, 4, logoWidth, logoHeight);

            const companyName = "PHARMACY AND MEDICINES REGULATORY AUTHORITY";
            doc.setFontSize(15);
            doc.setFont("bold");
            doc.text(companyName, 55.9, 18);
            const tagline = "ALL CORRESPONDENCE SHOULD BE ADDRESSED TO THE DIRECTOR GENERAL";
            doc.setFontSize(10.8).text(tagline, 55.9, 24);
            const title = "LOCAL PURCHASE ORDER";
            doc.setFontSize(15).text(title, 75.9, 34);
            doc.text("No.", 150, 34);
            const purchaseOrdernumber = `${this.getYear(purchase_order.purchase_order_date)}0000${purchase_order.id}`;
            doc.setFont("helvetica", "bold");
            doc.setFontSize(14).text(purchaseOrdernumber, 160, 34);
            doc.setFont("helvetica", "normal");
            const purchaseDate = `Date: ${this.formatDate(purchase_order.purchase_order_date)}`;
            doc.setFontSize(13).text(purchaseDate, 150, 40);
            doc.setFont("helvetica", "normal");

            doc.setFont("helvetica", "normal");
            doc.setFontSize(12).text("P.O Box 30241", 140, 52);
            doc.setFontSize(12).text("Capital City, Lilongwe 3, Malawi", 140, 57);
            doc.setFontSize(12).text("Phone: 212 755 165", 140, 62);
            doc.setFontSize(12).text("Email: info@pmra.mw", 140, 67);
            doc.setFontSize(12).text("Website: www.pmra.mw", 140, 72);

            doc.setFont("helvetica", "bold");
            doc.text("TO:", 14, 52);
            doc.setFont("helvetica", "normal");
            const supplierName = `${supplier.supplier}`;
            doc.setFontSize(12).text(supplierName, 22.86, 52);
            const supplierAddress = `${supplier.address}`;
            doc.setFontSize(12).text(supplierAddress, 22.86, 57);
        },
        requestItemsTable(doc) {
            doc.setFont("helvetica", "normal");
            const { purchase_order_items } = this.purchase_order_data;
            const subtotal = purchase_order_items.reduce((acc, item) => acc + item.amount * item.quantity, 0);
            const vatRate = 0.15;
            const vat = subtotal * vatRate;
            const total = subtotal + vat;

            const currencyFormatter = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'MWK',
            });

            const tableData1 = [
                ["Qty", "Item", "Description", "Unit Cost", "Amount"],
                ...purchase_order_items.map((item) => [item.quantity, item.item, item.description, currencyFormatter.format(item.amount), currencyFormatter.format(item.amount * item.quantity)]),
                ["", "", "", "Subtotal:", currencyFormatter.format(subtotal)],
                ["", "", "", "VAT (15%):", currencyFormatter.format(vat)],
                ["", "", "", "TOTAL:", currencyFormatter.format(total)],
            ];
            const yPos1 = 72;
            doc.setFontSize(12).text("Please supply the following", 14, yPos1);
            doc.autoTable({
                head: [tableData1[0]],
                body: tableData1.slice(1),
                startY: yPos1 + 2.54,
            });
        },
        addSignatureSpace(doc, yPos) {
            const lineY = yPos + 25.4;
            doc.setDrawColor(0);
            doc.setLineWidth(1.016);
            doc.line(14, lineY, 200, lineY);

            doc.setFontSize(12);
            doc.text("Signature: ___________________________________", 14, lineY + 18);
            doc.text("Date: _____________________________", 120, lineY + 18);
            doc.text("Signature: ___________________________________", 14, lineY + 38);
            doc.text("Date: _____________________________", 120, lineY + 38);
            doc.setFont("helvetica", "bold");
            doc.text("for DIRECTOR GENERAL", 14, lineY + 48);
        },
        savePDF(doc) {
            const { purchase_order } = this.purchase_order_data;
            doc.save(`LPO ${this.getYear(purchase_order.purchase_order_date)}0000${purchase_order.id}.pdf`);
        },
        getYear(dateString) {
            const date = new Date(dateString);
            const year = date.getFullYear();
            return year;
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const formattedDate = date.toLocaleString("en-US", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
            });
            return formattedDate;
        },
    },
};
</script>
