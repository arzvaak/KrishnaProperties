<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { ArrowRight } from "lucide-svelte";
    import { reveal } from "$lib/actions/reveal";
    import PropertyCard from "$lib/components/PropertyCard.svelte";

    export let properties: any[] = [];
    export let loading = true;
</script>

<section class="py-32 container px-4">
    <div class="flex justify-between items-end mb-16" use:reveal>
        <div>
            <h2 class="text-4xl md:text-5xl font-bold mb-4 text-foreground">
                Featured Collections
            </h2>
            <p class="text-xl text-muted-foreground max-w-xl">
                Handpicked properties that define luxury and comfort.
            </p>
        </div>
        <Button
            variant="outline"
            class="hidden md:flex gap-2"
            href="/properties"
        >
            View All Properties <ArrowRight class="w-4 h-4" />
        </Button>
    </div>

    {#if loading}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {#each Array(3) as _}
                <Skeleton class="h-[500px] w-full rounded-3xl" />
            {/each}
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {#each properties as property}
                <div class="group relative" use:reveal={{ threshold: 0.1 }}>
                    <PropertyCard {property} />
                </div>
            {/each}
        </div>
    {/if}

    <div class="mt-12 text-center md:hidden">
        <Button variant="outline" size="lg" class="w-full" href="/properties"
            >View All Properties</Button
        >
    </div>
</section>
