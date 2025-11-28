<script lang="ts">
    import { onMount } from "svelte";
    import { reveal } from "$lib/actions/reveal";
    import { API_BASE_URL } from "$lib/config";

    let stats = {
        properties: 150,
        clients: 2000,
        cities: 50,
        support: "24/7",
    };

    onMount(async () => {
        try {
            const res = await fetch(
                `${API_BASE_URL}/api/analytics/public-stats`,
            );
            if (res.ok) {
                const data = await res.json();
                stats = { ...stats, ...data };
            }
        } catch (e) {
            console.error("Failed to fetch stats", e);
        }
    });
</script>

<div
    class="mt-12 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto text-white/90"
>
    <div class="text-center group" use:reveal={{ delay: 100 }}>
        <div
            class="text-3xl font-bold mb-1 group-hover:text-amber-400 transition-colors"
        >
            {stats.properties}+
        </div>
        <div class="text-xs uppercase tracking-wider opacity-70">
            Premium Listings
        </div>
    </div>
    <div class="text-center group" use:reveal={{ delay: 200 }}>
        <div
            class="text-3xl font-bold mb-1 group-hover:text-amber-400 transition-colors"
        >
            {stats.clients}+
        </div>
        <div class="text-xs uppercase tracking-wider opacity-70">
            Happy Clients
        </div>
    </div>
    <div class="text-center group" use:reveal={{ delay: 300 }}>
        <div
            class="text-3xl font-bold mb-1 group-hover:text-amber-400 transition-colors"
        >
            {stats.cities}+
        </div>
        <div class="text-xs uppercase tracking-wider opacity-70">Cities</div>
    </div>
    <div class="text-center group" use:reveal={{ delay: 400 }}>
        <div
            class="text-3xl font-bold mb-1 group-hover:text-amber-400 transition-colors"
        >
            {stats.support}
        </div>
        <div class="text-xs uppercase tracking-wider opacity-70">Support</div>
    </div>
</div>
