<script lang="ts">
    import { comparison } from "$lib/stores/comparison";
    import { onMount } from "svelte";
    import { API_BASE_URL } from "$lib/config";
    import { Button } from "$lib/components/ui/button";
    import { Check, X, Loader2 } from "lucide-svelte";
    import AddToCompareButton from "./AddToCompareButton.svelte";

    export let currentProperty: any;

    let comparisonProperties: any[] = [];
    let loading = false;

    $: otherIds = $comparison.filter((id) => id !== currentProperty.id);

    // Fetch details when comparison list changes
    $: if (otherIds.length > 0) {
        loadComparisonData(otherIds);
    } else {
        comparisonProperties = [];
    }

    async function loadComparisonData(ids: string[]) {
        loading = true;
        try {
            // In a real app, use a batch fetch endpoint.
            // Here we fetch individually for simplicity.
            const promises = ids.map((id) =>
                fetch(`${API_BASE_URL}/api/properties/${id}`).then((r) =>
                    r.json(),
                ),
            );
            comparisonProperties = await Promise.all(promises);
        } catch (e) {
            console.error("Failed to load comparison data", e);
        } finally {
            loading = false;
        }
    }

    const features = [
        { label: "Price", key: "price" },
        { label: "Location", key: "location" },
        { label: "Type", key: "type" },
        { label: "Bedrooms", key: "bedrooms" },
        { label: "Bathrooms", key: "bathrooms" },
        { label: "Area", key: "area", format: (v: any) => `${v} sqft` },
    ];
</script>

{#if otherIds.length > 0}
    <div class="mt-12 border-t pt-12">
        <h2 class="text-2xl font-bold mb-6">Compare with Selected</h2>

        <div class="overflow-x-auto pb-4">
            <table class="w-full min-w-[600px] border-collapse">
                <thead>
                    <tr>
                        <th
                            class="p-4 text-left w-1/4 bg-gray-50/50 rounded-tl-lg"
                            >Feature</th
                        >
                        <!-- Current Property -->
                        <th
                            class="p-4 text-left w-1/4 bg-primary/5 border-l-4 border-primary"
                        >
                            <div class="font-bold text-lg text-primary">
                                This Property
                            </div>
                            <div class="text-sm font-medium truncate">
                                {currentProperty.title}
                            </div>
                        </th>
                        <!-- Other Properties -->
                        {#each comparisonProperties as prop}
                            <th class="p-4 text-left w-1/4">
                                <div
                                    class="font-bold text-lg truncate"
                                    title={prop.title}
                                >
                                    {prop.title}
                                </div>
                                <div class="mt-2">
                                    <AddToCompareButton
                                        propertyId={prop.id}
                                        size="sm"
                                    />
                                </div>
                            </th>
                        {/each}
                        <!-- Fill empty slots -->
                        {#each Array(3 - 1 - comparisonProperties.length) as _}
                            <th class="p-4 w-1/4"></th>
                        {/each}
                    </tr>
                </thead>
                <tbody class="divide-y">
                    {#each features as feature}
                        <tr class="hover:bg-gray-50/50 transition-colors">
                            <td class="p-4 font-medium text-muted-foreground"
                                >{feature.label}</td
                            >
                            <!-- Current -->
                            <td
                                class="p-4 font-semibold bg-primary/5 border-l-4 border-primary"
                            >
                                {feature.format
                                    ? feature.format(
                                          currentProperty[feature.key],
                                      )
                                    : currentProperty[feature.key] || "-"}
                            </td>
                            <!-- Others -->
                            {#each comparisonProperties as prop}
                                <td class="p-4">
                                    {feature.format
                                        ? feature.format(prop[feature.key])
                                        : prop[feature.key] || "-"}
                                </td>
                            {/each}
                            {#each Array(3 - 1 - comparisonProperties.length) as _}
                                <td class="p-4"></td>
                            {/each}
                        </tr>
                    {/each}
                    <!-- Image Row -->
                    <tr>
                        <td class="p-4 font-medium text-muted-foreground"
                            >Image</td
                        >
                        <td class="p-4 bg-primary/5 border-l-4 border-primary">
                            <img
                                src={currentProperty.imageUrl}
                                alt={currentProperty.title}
                                class="w-full h-24 object-cover rounded-md"
                            />
                        </td>
                        {#each comparisonProperties as prop}
                            <td class="p-4">
                                <img
                                    src={prop.imageUrl}
                                    alt={prop.title}
                                    class="w-full h-24 object-cover rounded-md"
                                />
                            </td>
                        {/each}
                        {#each Array(3 - 1 - comparisonProperties.length) as _}
                            <td class="p-4"></td>
                        {/each}
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
{/if}
