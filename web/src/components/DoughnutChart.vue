<template>
    <div class="w-full h-full">
        <Doughnut id="my-chart-id" :options="chartOptions" :data="chartData" />
    </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs'

export default {
    name: 'DoughnutChart',
    components: { Doughnut },
    props: {
        totalBudget: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            chartData: {
                labels: ['Balance', 'Expenditure'],
                datasets: [
                    {
                        backgroundColor: ['#00D8FF', '#DD1B16'],
                        data: [80, 20]
                    }
                ]
            },
            chartOptions: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Budget expenditure',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    }
}
</script>
