<script lang="ts">
    import { Line, Bar, Doughnut } from "svelte-chartjs";
    import {
        Chart as ChartJS,
        Title,
        Tooltip,
        Legend,
        LineElement,
        LinearScale,
        PointElement,
        CategoryScale,
        BarElement,
        ArcElement,
    } from "chart.js";

    ChartJS.register(
        Title,
        Tooltip,
        Legend,
        LineElement,
        LinearScale,
        PointElement,
        CategoryScale,
        BarElement,
        ArcElement,
    );

    export let trafficStats: any[] = [];
    export let funnel: any = {};
    export let topProperties: any[] = [];

    // Traffic Chart Data
    $: trafficData = {
        labels: trafficStats.map((s) => s.date),
        datasets: [
            {
                label: "Site Views",
                data: trafficStats.map((s) => s.count),
                borderColor: "rgb(75, 192, 192)",
                backgroundColor: "rgba(75, 192, 192, 0.5)",
                tension: 0.3,
            },
        ],
    };

    // Funnel Chart Data
    $: funnelData = {
        labels: ["New", "Contacted", "Qualified", "Converted", "Lost"],
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
    };

    // Top Properties Chart Data
    $: topPropertiesData = {
        labels: topProperties.map((p) =>
            p.title.length > 20 ? p.title.substring(0, 20) + "..." : p.title,
        ),
        datasets: [
            {
                label: "Views",
                data: topProperties.map((p) => p.views),
                backgroundColor: "rgba(255, 159, 64, 0.6)",
            },
        ],
    };
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <!-- Traffic Chart -->
    <div class="bg-card p-6 rounded-xl border shadow-sm">
        <h3 class="text-lg font-semibold mb-4">
            Traffic Overview (Last 30 Days)
        </h3>
        <div class="h-[300px]">
            <Line
                data={trafficData}
                options={{ maintainAspectRatio: false, responsive: true }}
            />
        </div>
    </div>

    <!-- Funnel Chart -->
    <div class="bg-card p-6 rounded-xl border shadow-sm">
        <h3 class="text-lg font-semibold mb-4">Lead Conversion Funnel</h3>
        <div class="h-[300px] flex justify-center">
            <Doughnut
                data={funnelData}
                options={{ maintainAspectRatio: false, responsive: true }}
            />
        </div>
    </div>

    <!-- Top Properties Chart -->
    <div class="bg-card p-6 rounded-xl border shadow-sm lg:col-span-2">
        <h3 class="text-lg font-semibold mb-4">Most Viewed Properties</h3>
        <div class="h-[300px]">
            <Bar
                data={topPropertiesData}
                options={{
                    maintainAspectRatio: false,
                    responsive: true,
                    indexAxis: "y",
                }}
            />
        </div>
    </div>
</div>
