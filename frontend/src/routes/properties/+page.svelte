<script lang="ts">
  import { onMount } from "svelte";
  import PropertyCard from "$lib/components/PropertyCard.svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import { Label } from "$lib/components/ui/label";
  import * as Select from "$lib/components/ui/select";
  import { Slider } from "$lib/components/ui/slider";
  import { Badge } from "$lib/components/ui/badge";
  import { Filter, X } from "lucide-svelte";
  import { fade, slide } from "svelte/transition";

  let properties: any[] = [];
  let loading = true;
  let error = null;

  // Filters
  let searchQuery = "";
  let minPrice = 0;
  let maxPrice = 100000000; // 10 Cr
  let bedrooms = 0;
  let propertyType = "all";
  let showFilters = false;

  async function fetchProperties() {
    loading = true;
    error = null;
    try {
      const params = new URLSearchParams();
      if (searchQuery) params.append("search", searchQuery);
      if (minPrice > 0) params.append("min_price", minPrice.toString());
      if (maxPrice < 100000000) params.append("max_price", maxPrice.toString());
      if (bedrooms > 0) params.append("bedrooms", bedrooms.toString());
      if (propertyType && propertyType !== "all")
        params.append("type", propertyType);

      const response = await fetch(
        `http://127.0.0.1:5000/api/properties?${params.toString()}`,
      );
      if (!response.ok) throw new Error("Failed to fetch properties");
      properties = await response.json();
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function formatPrice(price: number) {
    if (price >= 10000000) return `₹ ${(price / 10000000).toFixed(1)} Cr`;
    if (price >= 100000) return `₹ ${(price / 100000).toFixed(1)} L`;
    return `₹ ${price.toLocaleString()}`;
  }

  function clearFilters() {
    searchQuery = "";
    minPrice = 0;
    maxPrice = 100000000;
    bedrooms = 0;
    propertyType = "all";
    fetchProperties();
  }

  onMount(() => {
    fetchProperties();
  });
</script>

<div class="container py-8">
  <div class="flex flex-col gap-6 mb-8">
    <div
      class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
    >
      <div>
        <h1 class="text-4xl font-bold mb-2 tracking-tight">Properties</h1>
        <p class="text-muted-foreground text-lg">
          Explore our curated list of premium homes
        </p>
      </div>
      <div class="flex gap-2 w-full md:w-auto">
        <div class="relative w-full md:w-[300px]">
          <Input
            placeholder="Search location, title..."
            bind:value={searchQuery}
            onkeydown={(e) => e.key === "Enter" && fetchProperties()}
            class="w-full"
          />
        </div>
        <Button onclick={fetchProperties}>Search</Button>
        <Button
          variant="outline"
          size="icon"
          onclick={() => (showFilters = !showFilters)}
          class={showFilters ? "bg-secondary" : ""}
        >
          <Filter class="w-4 h-4" />
        </Button>
      </div>
    </div>

    {#if showFilters}
      <div
        transition:slide
        class="bg-card border rounded-xl p-6 shadow-sm grid grid-cols-1 md:grid-cols-4 gap-6"
      >
        <div class="space-y-2">
          <Label>Property Type</Label>
          <Select.Root
            type="single"
            bind:value={propertyType}
            onValueChange={() => setTimeout(fetchProperties, 100)}
          >
            <Select.Trigger>
              {propertyType === "all" ? "Any Type" : propertyType}
            </Select.Trigger>
            <Select.Content>
              <Select.Item value="all">Any Type</Select.Item>
              <Select.Item value="Apartment">Apartment</Select.Item>
              <Select.Item value="Villa">Villa</Select.Item>
              <Select.Item value="Penthouse">Penthouse</Select.Item>
              <Select.Item value="Plot">Plot</Select.Item>
            </Select.Content>
          </Select.Root>
        </div>

        <div class="space-y-2">
          <Label>Bedrooms: {bedrooms === 0 ? "Any" : `${bedrooms}+`}</Label>
          <Slider
            type="multiple"
            value={[bedrooms]}
            min={0}
            max={5}
            step={1}
            onValueChange={(v: number[]) => {
              bedrooms = v[0];
              fetchProperties();
            }}
            class="py-4"
          />
        </div>

        <div class="space-y-2 md:col-span-2">
          <Label>
            Price Range: {formatPrice(minPrice)} - {formatPrice(maxPrice)}
          </Label>
          <Slider
            type="multiple"
            value={[minPrice, maxPrice]}
            min={0}
            max={100000000}
            step={1000000}
            onValueChange={(v: number[]) => {
              minPrice = v[0];
              maxPrice = v[1];
              // Debounce fetch for slider
              const timeout = setTimeout(fetchProperties, 500);
              return () => clearTimeout(timeout);
            }}
            class="py-4"
          />
        </div>

        <div class="md:col-span-4 flex justify-end">
          <Button
            variant="ghost"
            size="sm"
            onclick={clearFilters}
            class="text-muted-foreground hover:text-foreground"
          >
            <X class="w-4 h-4 mr-2" /> Clear Filters
          </Button>
        </div>
      </div>
    {/if}

    <!-- Active Filters Badges -->
    {#if minPrice > 0 || maxPrice < 100000000 || bedrooms > 0 || (propertyType && propertyType !== "all")}
      <div class="flex flex-wrap gap-2">
        {#if propertyType && propertyType !== "all"}
          <Badge variant="secondary" class="px-3 py-1"
            >Type: {propertyType}</Badge
          >
        {/if}
        {#if bedrooms > 0}
          <Badge variant="secondary" class="px-3 py-1">{bedrooms}+ Beds</Badge>
        {/if}
        {#if minPrice > 0 || maxPrice < 100000000}
          <Badge variant="secondary" class="px-3 py-1"
            >Price: {formatPrice(minPrice)} - {formatPrice(maxPrice)}</Badge
          >
        {/if}
      </div>
    {/if}
  </div>

  {#if loading}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {#each Array(6) as _}
        <div class="space-y-4">
          <Skeleton class="h-[300px] w-full rounded-2xl" />
          <div class="space-y-2">
            <Skeleton class="h-6 w-[250px]" />
            <Skeleton class="h-4 w-[200px]" />
          </div>
        </div>
      {/each}
    </div>
  {:else if error}
    <div
      class="text-center py-20 text-red-500 bg-red-50 rounded-xl border border-red-100"
    >
      <p class="font-medium">Error loading properties</p>
      <p class="text-sm opacity-80 mb-4">{error}</p>
      <Button variant="outline" onclick={fetchProperties}>Try Again</Button>
    </div>
  {:else if properties.length === 0}
    <div class="text-center py-32 bg-muted/30 rounded-3xl border border-dashed">
      <div
        class="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4"
      >
        <Filter class="w-8 h-8 text-muted-foreground" />
      </div>
      <h3 class="text-xl font-bold mb-2">No properties found</h3>
      <p class="text-muted-foreground mb-6">
        Try adjusting your search or filters to find what you're looking for.
      </p>
      <Button onclick={clearFilters}>Clear All Filters</Button>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {#each properties as property (property.id)}
        <div transition:fade>
          <PropertyCard {property} />
        </div>
      {/each}
    </div>
  {/if}
</div>
