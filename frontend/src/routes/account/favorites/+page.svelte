<script lang="ts">
    import { onMount } from "svelte";
    import { user, loading as authLoading } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import PropertyCard from "$lib/components/PropertyCard.svelte";
    import { Skeleton } from "$lib/components/ui/skeleton";

    let favorites: any[] = [];
    let loading = true;

    onMount(() => {
        const unsubscribe = user.subscribe(async (u) => {
            if (!authLoading && !u) {
                goto("/login");
                return;
            }

            if (u) {
                try {
                    const response = await fetch(
                        `http://127.0.0.1:5000/api/users/${u.uid}/favorites`,
                    );
                    if (response.ok) {
                        favorites = await response.json();
                    }
                } catch (error) {
                    console.error("Failed to fetch favorites:", error);
                } finally {
                    loading = false;
                }
            }
        });
        return unsubscribe;
    });
</script>

<div class="container py-8">
    <h1 class="text-3xl font-bold mb-8">Saved Properties</h1>

    {#if loading}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(3) as _}
                <div class="space-y-4">
                    <Skeleton class="h-[200px] w-full rounded-xl" />
                    <div class="space-y-2">
                        <Skeleton class="h-4 w-[250px]" />
                        <Skeleton class="h-4 w-[200px]" />
                    </div>
                </div>
            {/each}
        </div>
    {:else if favorites.length === 0}
        <div class="text-center py-20">
            <p class="text-muted-foreground text-lg mb-4">
                You haven't saved any properties yet.
            </p>
            <a href="/properties" class="text-primary hover:underline"
                >Browse Properties</a
            >
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each favorites as property}
                <PropertyCard {property} />
            {/each}
        </div>
    {/if}
</div>
