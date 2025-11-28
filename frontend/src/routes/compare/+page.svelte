<script lang="ts">
    import { comparison } from "$lib/stores/comparison";
    import { API_BASE_URL } from "$lib/config";
    import { Button } from "$lib/components/ui/button";
    import { X, Check, ArrowLeft } from "lucide-svelte";
    import { fade } from "svelte/transition";

    let properties: any[] = [];
    let loading = false;

    $: ids = $comparison;

    $: if (ids.length > 0) {
        loadProperties(ids);
    } else {
        properties = [];
    }

    async function loadProperties(ids: string[]) {
        loading = true;
        try {
            const promises = ids.map((id) =>
                fetch(`${API_BASE_URL}/api/properties/${id}`).then((r) =>
                    r.json(),
                ),
            );
            properties = await Promise.all(promises);
        } catch (e) {
            console.error("Failed to load properties", e);
        } finally {
            loading = false;
        }
    }

    function remove(id: string) {
        comparison.removeProperty(id);
    }

    const features = [
        { label: "Price", key: "price" },
        { label: "Location", key: "location" },
        { label: "Type", key: "type" },
        { label: "Bedrooms", key: "bedrooms" },
        { label: "Bathrooms", key: "bathrooms" },
        { label: "Area", key: "area", format: (v: any) => `${v} sqft` },
        { label: "Status", key: "status" },
    ];
</script>

<div class="container py-12 min-h-[80vh]">
    <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-4">
            <Button variant="ghost" href="/properties">
                <ArrowLeft class="w-4 h-4 mr-2" /> Back to Properties
            </Button>
            <h1 class="text-3xl font-bold">Compare Properties</h1>
        </div>
        {#if properties.length > 0}
            <Button variant="outline" onclick={() => comparison.clear()}>
                Clear All
            </Button>
        {/if}
    </div>

    {#if properties.length === 0}
        <div class="text-center py-20 bg-muted/30 rounded-3xl">
            <h3 class="text-xl font-semibold mb-2">No properties selected</h3>
            <p class="text-muted-foreground mb-6">
                Add properties to compare them side by side.
            </p>
            <Button href="/properties">Browse Properties</Button>
        </div>
    {:else if loading}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {#each Array(3) as _}
                <div class="h-[600px] bg-muted animate-pulse rounded-xl"></div>
            {/each}
        </div>
    {:else}
        <div class="overflow-x-auto pb-8">
            <table class="w-full min-w-[800px] border-collapse">
                <thead>
                    <tr>
                        <th class="p-4 w-48"></th>
                        {#each properties as prop}
                            <th class="p-4 w-1/3 min-w-[300px] align-top">
                                <div class="relative group">
                                    <div
                                        class="aspect-[4/3] rounded-xl overflow-hidden mb-4"
                                    >
                                        <img
                                            src={prop.imageUrl ||
                                                prop.images?.[0]}
                                            alt={prop.title}
                                            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                        />
                                        <button
                                            class="absolute top-2 right-2 p-1.5 bg-black/50 hover:bg-red-500 text-white rounded-full backdrop-blur-sm transition-colors"
                                            onclick={() => remove(prop.id)}
                                            title="Remove"
                                        >
                                            <X class="w-4 h-4" />
                                        </button>
                                    </div>
                                    <h3
                                        class="text-xl font-bold mb-1 line-clamp-1"
                                        title={prop.title}
                                    >
                                        <a
                                            href="/properties/{prop.id}"
                                            class="hover:text-primary transition-colors"
                                        >
                                            {prop.title}
                                        </a>
                                    </h3>
                                    <p class="text-muted-foreground mb-3">
                                        {prop.location}
                                    </p>
                                    <div class="flex gap-2">
                                        <Button
                                            class="w-full"
                                            href="/properties/{prop.id}"
                                        >
                                            View Details
                                        </Button>
                                    </div>
                                </div>
                            </th>
                        {/each}
                        {#each Array(3 - properties.length) as _}
                            <th
                                class="p-4 w-1/3 bg-muted/10 rounded-xl border-2 border-dashed border-muted-foreground/20"
                            >
                                <div
                                    class="h-full flex flex-col items-center justify-center text-muted-foreground py-20"
                                >
                                    <p class="mb-4">Add another property</p>
                                    <Button variant="outline" href="/properties"
                                        >Browse</Button
                                    >
                                </div>
                            </th>
                        {/each}
                    </tr>
                </thead>
                <tbody class="divide-y">
                    {#each features as feature}
                        <tr class="hover:bg-muted/30 transition-colors">
                            <td class="p-4 font-medium text-muted-foreground"
                                >{feature.label}</td
                            >
                            {#each properties as prop}
                                <td class="p-4 font-semibold text-lg">
                                    {feature.format
                                        ? feature.format(prop[feature.key])
                                        : prop[feature.key] || "-"}
                                </td>
                            {/each}
                            {#each Array(3 - properties.length) as _}
                                <td class="p-4"></td>
                            {/each}
                        </tr>
                    {/each}
                    <!-- Amenities -->
                    <tr>
                        <td
                            class="p-4 font-medium text-muted-foreground align-top pt-8"
                            >Amenities</td
                        >
                        {#each properties as prop}
                            <td class="p-4 align-top pt-8">
                                <div class="flex flex-wrap gap-2">
                                    {#each prop.amenities || [] as amenity}
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary"
                                        >
                                            {amenity}
                                        </span>
                                    {/each}
                                </div>
                            </td>
                        {/each}
                        {#each Array(3 - properties.length) as _}
                            <td class="p-4"></td>
                        {/each}
                    </tr>
                </tbody>
            </table>
        </div>
    {/if}
</div>
