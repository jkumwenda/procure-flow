<template>
    <div class="w-full h-full">
        <Bar id="my-chart-id" :options="chartOptions" :data="chartData" :width="chartWidth" :height="chartHeight" />
    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'

export default {
    name: 'BarChart',
    components: { Bar },
    data() {
        return {
            chartData: {
                labels: ['Mon', 'Tue', 'Wed', "Thu", "Fri", "Sat", "Sun"],
                datasets: [{ data: [40, 10, 28, 32, 6, 8, 60] }]
            },
            chartWidth: 300, // Specify the desired width
            chartHeight: 220, // Specify the desired height
            chartOptions: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false // Hide the legend
                    },
                    tooltip: {
                        enabled: true,
                        mode: 'index', // Show tooltips for multiple bars at the same index
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)', // Tooltip background color
                        titleFontColor: 'white', // Title text color
                        bodyFontColor: 'white', // Body text color
                        titleSpacing: 4, // Spacing between title and body
                        bodySpacing: 8, // Spacing between body lines
                        borderWidth: 1, // Tooltip border width
                        borderColor: 'rgba(255, 255, 255, 0.2)', // Tooltip border color
                    },
                    title: {
                        display: true,
                        text: 'Total requests last week',
                        padding: {
                            top: 10,
                            bottom: 20
                        },
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: false,
                            text: 'Days of week',
                            font: {
                                size: 16, // Font size in pixels
                                family: 'Arial, sans-serif', // Font family
                                style: 'light', // Font style (normal, italic, or oblique)
                            },
                        },
                        grid: {
                            display: false // Hide X-axis grid lines
                        },
                        ticks: {
                            font: {
                                size: 12, // Font size in pixels
                                family: 'Arial, sans-serif', // Font family
                                style: 'light', // Font style (normal, italic, or oblique)
                            },
                        },
                    },
                    y: {
                        title: {
                            display: false,
                            text: 'Value',
                            font: {
                                size: 16, // Font size in pixels
                                family: 'Arial, sans-serif', // Font family
                                style: 'normal', // Font style (normal, italic, or oblique)
                            },
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)' // Y-axis grid line color
                        },
                        ticks: {
                            font: {
                                size: 12, // Font size in pixels
                                family: 'Arial, sans-serif', // Font family
                                style: 'normal', // Font style (normal, italic, or oblique)
                            },
                        },
                    }
                },
                elements: {
                    bar: {
                        backgroundColor: '#FFB1C1',
                        borderColor: '#FF6384',
                        borderWidth: 2,
                        borderRadius: 18,
                    }
                },
                // Other options...
            }
        }
    }
}
</script>