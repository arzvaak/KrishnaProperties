<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Chart from "chart.js/auto";

    export let trafficStats: any[] = [];
    export let funnel: any = {};
    export let topProperties: any[] = [];

    let trafficChartCanvas: HTMLCanvasElement;
    let funnelChartCanvas: HTMLCanvasElement;
    let topPropertiesChartCanvas: HTMLCanvasElement;

    let trafficChart: Chart | null = null;
    let funnelChart: Chart | null = null;
    let topPropertiesChart: Chart | null = null;

    function updateCharts() {
        if (trafficChart) trafficChart.destroy();
        if (funnelChart) funnelChart.destroy();
        if (topPropertiesChart) topPropertiesChart.destroy();

        if (trafficChartCanvas) {
            trafficChart = new Chart(trafficChartCanvas, {
                type: "line",
                data: {
                    labels: trafficStats.map((s) => s.date),
                    datasets: [
                        {
                            label: "Site Views",
                            data: trafficStats.map((s) => s.count),
                            borderColor: "rgb(75, 192, 192)",
                            backgroundColor: "rgba(75, 192, 192, 0.5)",
                            tension: 0.3,
                            fill: true,
                        },
                    ],
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                },
            });
        }

        if (funnelChartCanvas) {
            funnelChart = new Chart(funnelChartCanvas, {
                type: "doughnut",
                data: {
                    labels: [
                        "New",
                        "Contacted",
                        "Qualified",
                        "Converted",
                        "Lost",
                    ],
                    datasets: [
                        {
                            label: "Leads",
                            data: [
                                funnel.new || 0,
                                funnel.contacted || 0,
                                funnel.qualified || 0,
                                funnel.converted || 0,
                                funnel.lost || 0,
                            ],
                            backgroundColor: [
                                "rgba(54, 162, 235, 0.6)",
                                "rgba(255, 206, 86, 0.6)",
                                "rgba(75, 192, 192, 0.6)",
                                "rgba(153, 102, 255, 0.6)",
                                "rgba(255, 99, 132, 0.6)",
                            ],
                        },
                    ],
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                },
            });
        }

        if (topPropertiesChartCanvas) {
            topPropertiesChart = new Chart(topPropertiesChartCanvas, {
                type: "bar",
                data: {
                    labels: topProperties.map((p) =>
                        p.title.length > 20
                            ? p.title.substring(0, 20) + "..."
                            : p.title,
                    ),
                    datasets: [
                        {
                            label: "Views",
                            data: topProperties.map((p) => p.views),
                            backgroundColor: "rgba(255, 159, 64, 0.6)",
                        },
                    ],
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    indexAxis: "y",
                },
            });
        }
    }

    onMount(() => {
        updateCharts();
    });

    onDestroy(() => {
        if (trafficChart) trafficChart.destroy();
        if (funnelChart) funnelChart.destroy();
        if (topPropertiesChart) topPropertiesChart.destroy();
    });

    $: {
        if (trafficStats || funnel || topProperties) {
            // React to data changes
            // In a real app, we might want to update data instead of destroying/recreating
            // But for simplicity and robustness here:
            if (typeof window !== "undefined") {
                // Defer slightly to ensure canvas is ready if re-rendering
                setTimeout(updateCharts, 0);
            }
        }
    }
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <!-- Traffic Chart -->
    <div class="bg-card p-6 rounded-xl border shadow-sm">
        <h3 class="text-lg font-semibold mb-4">
            Traffic Overview (Last 30 Days)
        </h3>
        <div class="h-[300px]">
            <canvas bind:this={trafficChartCanvas}></canvas>
        </div>
    </div>

    <!-- Funnel Chart -->
    <div class="bg-card p-6 rounded-xl border shadow-sm">
        <h3 class="text-lg font-semibold mb-4">Lead Conversion Funnel</h3>
        <div class="h-[300px] flex justify-center">
            <canvas bind:this={funnelChartCanvas}></canvas>
        </div>
    </div>

    <!-- Top Properties Chart -->
    <div class="bg-card p-6 rounded-xl border shadow-sm lg:col-span-2">
        <h3 class="text-lg font-semibold mb-4">Most Viewed Properties</h3>
        <div class="h-[300px]">
            <canvas bind:this={topPropertiesChartCanvas}></canvas>
        </div>
    </div>
</div>
