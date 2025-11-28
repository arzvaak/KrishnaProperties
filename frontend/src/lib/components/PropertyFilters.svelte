<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import * as Select from "$lib/components/ui/select";
    import { Slider } from "$lib/components/ui/slider";
    import { Search, SlidersHorizontal, Save, History, X } from "lucide-svelte";
    import { slide } from "svelte/transition";
    import { user } from "$lib/stores/auth";

    export let searchQuery = "";
    export let minPrice = 0;
    export let maxPrice = 100000000;
    export let bedrooms = 0;
    export let propertyType = "all";
    export let showFilters = false;
    export let onSearch: () => void;
    export let onClear: () => void;
    export let onSaveSearch: () => void;
    export let onLoadSavedSearches: () => void;

    function formatPrice(price: number) {
        if (price >= 10000000) return `₹ ${(price / 10000000).toFixed(1)} Cr`;
        if (price >= 100000) return `₹ ${(price / 100000).toFixed(1)} L`;
        return `₹ ${price.toLocaleString()}`;
    }
</script>

<div
    class="bg-card/80 backdrop-blur-xl border border-white/20 rounded-2xl p-6 shadow-2xl mb-12"
>
    <div class="flex flex-col md:flex-row gap-4 items-center">
        <div class="relative flex-1 w-full">
            <Search
                class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground w-5 h-5"
            />
            <Input
                placeholder="Search by location, title..."
                bind:value={searchQuery}
                onkeydown={(e) => e.key === "Enter" && onSearch()}
                class="pl-10 h-12 bg-background/50 border-border/50 text-lg"
            />
        </div>

        <div class="flex gap-2 w-full md:w-auto">
            <Button onclick={onSearch} size="lg" class="h-12 px-8"
                >Search</Button
            >
            <Button
                variant="outline"
                size="lg"
                onclick={() => (showFilters = !showFilters)}
                class="h-12 px-4 {showFilters ? 'bg-secondary' : ''}"
            >
                <SlidersHorizontal class="w-5 h-5 mr-2" /> Filters
            </Button>
        </div>
    </div>

    <!-- Expanded Filters -->
    {#if showFilters}
        <div
            transition:slide
            class="pt-8 mt-6 border-t border-border/50 grid grid-cols-1 md:grid-cols-4 gap-8"
        >
            <div class="space-y-3">
                <Label class="text-base">Property Type</Label>
                <Select.Root
                    type="single"
                    bind:value={propertyType}
                    onValueChange={() => setTimeout(onSearch, 100)}
                >
                    <Select.Trigger class="h-10">
                        {propertyType === "all" ? "Any Type" : propertyType}
                    </Select.Trigger>
                    <Select.Content>
                        <Select.Item value="all">Any Type</Select.Item>
                        <Select.Item value="Authority plots"
                            >Authority plots</Select.Item
                        >
                        <Select.Item value="Free Hold plots"
                            >Free Hold plots</Select.Item
                        >
                        <Select.Item value="Commercial Plots"
                            >Commercial Plots</Select.Item
                        >
                        <Select.Item value="Industrial or Factory Plots"
                            >Industrial or Factory Plots</Select.Item
                        >
                        <Select.Item value="Villa's">Villa's</Select.Item>
                    </Select.Content>
                </Select.Root>
            </div>

            <div class="space-y-3">
                <Label class="text-base"
                    >Bedrooms: {bedrooms === 0 ? "Any" : `${bedrooms}+`}</Label
                >
                <Slider
                    type="multiple"
                    value={[bedrooms]}
                    min={0}
                    max={5}
                    step={1}
                    onValueChange={(v) => {
                        bedrooms = v[0];
                        onSearch();
                    }}
                    class="py-4"
                />
            </div>

            <div class="space-y-3 md:col-span-2">
                <Label class="text-base">
                    Price Range: {formatPrice(minPrice)} - {formatPrice(
                        maxPrice,
                    )}
                </Label>
                <Slider
                    type="multiple"
                    value={[minPrice, maxPrice]}
                    min={0}
                    max={100000000}
                    step={1000000}
                    onValueChange={(v) => {
                        minPrice = v[0];
                        maxPrice = v[1];
                        const timeout = setTimeout(onSearch, 500);
                        return () => clearTimeout(timeout);
                    }}
                    class="py-4"
                />
            </div>

            <div class="md:col-span-4 flex justify-between items-center pt-4">
                <div class="flex gap-2">
                    {#if $user}
                        <Button
                            variant="ghost"
                            size="sm"
                            onclick={onSaveSearch}
                        >
                            <Save class="w-4 h-4 mr-2" /> Save Search
                        </Button>
                        <Button
                            variant="ghost"
                            size="sm"
                            onclick={onLoadSavedSearches}
                        >
                            <History class="w-4 h-4 mr-2" /> Saved Searches
                        </Button>
                    {/if}
                </div>
                <Button
                    variant="ghost"
                    size="sm"
                    onclick={onClear}
                    class="text-destructive hover:text-destructive"
                >
                    <X class="w-4 h-4 mr-2" /> Clear Filters
                </Button>
            </div>
        </div>
    {/if}
</div>
