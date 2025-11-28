<script lang="ts">
    import { onMount } from "svelte";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import { Badge } from "$lib/components/ui/badge";
    import { Clock, History } from "lucide-svelte";
    import { formatDistanceToNow } from "date-fns";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    export let propertyId: string;

    let history: any[] = [];
    let loading = true;

    onMount(async () => {
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/properties/${propertyId}/history`,
            );
            if (res.ok) {
                history = await res.json();
            }
        } catch (e) {
            console.error("Failed to load history", e);
        } finally {
            loading = false;
        }
    });

    function getActionColor(action: string) {
        switch (action) {
            case "Price Change":
                return "bg-blue-100 text-blue-700";
            case "Property Updated":
                return "bg-yellow-100 text-yellow-700";
            case "Status Change":
                return "bg-purple-100 text-purple-700";
            default:
                return "bg-gray-100 text-gray-700";
        }
    }
</script>

<Card>
    <CardHeader>
        <CardTitle class="flex items-center gap-2">
            <History class="w-5 h-5" /> Property History
        </CardTitle>
    </CardHeader>
    <CardContent>
        {#if loading}
            <div class="text-center py-4 text-muted-foreground">
                Loading history...
            </div>
        {:else if history.length === 0}
            <div
                class="text-center py-8 text-muted-foreground bg-muted/30 rounded-lg"
            >
                No history available for this property.
            </div>
        {:else}
            <div class="relative pl-6 border-l border-border space-y-8">
                {#each history as item}
                    <div class="relative">
                        <div
                            class="absolute -left-[29px] top-1 w-3 h-3 rounded-full bg-primary border-4 border-background"
                        ></div>
                        <div class="flex flex-col gap-1">
                            <div class="flex items-center gap-2">
                                <span
                                    class={`text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider ${getActionColor(item.action)}`}
                                >
                                    {item.action}
                                </span>
                                <span
                                    class="text-xs text-muted-foreground flex items-center gap-1"
                                >
                                    <Clock class="w-3 h-3" />
                                    {item.timestamp
                                        ? formatDistanceToNow(
                                              new Date(item.timestamp),
                                              { addSuffix: true },
                                          )
                                        : "Unknown date"}
                                </span>
                            </div>
                            <p class="text-sm text-foreground mt-1">
                                {item.details}
                            </p>
                            <p class="text-xs text-muted-foreground">
                                Updated by: {item.userId}
                            </p>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </CardContent>
</Card>
