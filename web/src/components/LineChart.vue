<template>
    <div>
        <line-chart :chartData="chartData" :options="chartOptions"></line-chart>
    </div>
</template>

<script>
import LineChart from '@/components/LineChart.vue';

export default {
    components: {
        LineChart,
    },
    data() {
        return {
            chartData: {
                labels: ['January', 'February', 'March', 'April', 'May'],
                datasets: [
                    {
                        label: 'Sample Data',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        data: [65, 59, 80, 81, 56],
                    },
                ],
            },
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
            },
        };
    },
};
</script>
