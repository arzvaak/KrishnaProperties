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
  import { Filter, X, Save, History, Trash2 } from "lucide-svelte";
  import { fade, slide } from "svelte/transition";
  import { user } from "$lib/stores/auth";
  import * as Dialog from "$lib/components/ui/dialog";
  import { toast } from "svelte-sonner";

  let properties: any[] = [];
  let loading = true;
  let error: string | null = null;

  // Filters
  let searchQuery = "";
  let minPrice = 0;
  let maxPrice = 100000000; // 10 Cr
  let bedrooms = 0;
  let propertyType = "all";
  let showFilters = false;
  let sortBy = "newest";
  let currentPage = 1;
  let totalPages = 1;
  let totalProperties = 0;

  // Saved Searches & Recently Viewed
  let isSaveSearchOpen = false;
  let isSavedSearchesListOpen = false;
  let searchName = "";
  let savedSearches: any[] = [];
  let recentlyViewed: any[] = [];

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

      params.append("sort", sortBy);
      params.append("page", currentPage.toString());

      const response = await fetch(
        `http://127.0.0.1:5000/api/properties?${params.toString()}`,
      );
      if (!response.ok) throw new Error("Failed to fetch properties");
      const data = await response.json();
      properties = data.properties;
      totalPages = data.total_pages;
      currentPage = data.page;
      totalProperties = data.total;
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
    currentPage = 1;
    fetchProperties();
  }

  function handleSortChange(value: string) {
    sortBy = value;
    currentPage = 1; // Reset to first page on sort change
    fetchProperties();
  }

  function handlePageChange(page: number) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    fetchProperties();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function saveSearch() {
    if (!$user) {
      toast.error("Please login to save searches");
      return;
    }
    if (!searchName) return;

    try {
      const filters = {
        searchQuery,
        minPrice,
        maxPrice,
        bedrooms,
        propertyType,
        sortBy,
      };

      const res = await fetch(
        `http://127.0.0.1:5000/api/users/${$user.uid}/saved-searches`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: searchName, filters }),
        },
      );

      if (!res.ok) throw new Error("Failed to save search");

      toast.success("Search saved successfully");
      isSaveSearchOpen = false;
      searchName = "";
    } catch (e: any) {
      toast.error(e.message);
    }
  }

  async function loadSavedSearches() {
    if (!$user) return;
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/users/${$user.uid}/saved-searches`,
      );
      if (res.ok) {
        savedSearches = await res.json();
        isSavedSearchesListOpen = true;
      }
    } catch (e) {
      console.error(e);
    }
  }

  function applySearch(search: any) {
    const f = search.filters;
    searchQuery = f.searchQuery || "";
    minPrice = f.minPrice || 0;
    maxPrice = f.maxPrice || 100000000;
    bedrooms = f.bedrooms || 0;
    propertyType = f.propertyType || "all";
    sortBy = f.sortBy || "newest";
    isSavedSearchesListOpen = false;
    fetchProperties();
    toast.success("Filters applied");
  }

  async function deleteSearch(id: string) {
    if (!$user) return;
    try {
      await fetch(
        `http://127.0.0.1:5000/api/users/${$user.uid}/saved-searches/${id}`,
        {
          method: "DELETE",
        },
      );
      savedSearches = savedSearches.filter((s) => s.id !== id);
      toast.success("Search deleted");
    } catch (e) {
      toast.error("Failed to delete search");
    }
  }

  onMount(() => {
    fetchProperties();

    // Load recently viewed
    user.subscribe(async (u) => {
      if (u) {
        // Logged in: Fetch from API
        try {
          const res = await fetch(
            `http://127.0.0.1:5000/api/users/${u.uid}/recently-viewed`,
          );
          if (res.ok) {
            recentlyViewed = await res.json();
          }
        } catch (e) {
          console.error("Failed to fetch recently viewed from API", e);
        }
      } else {
        // Guest: Fetch from localStorage
        const viewed = localStorage.getItem("recentlyViewed");
        if (viewed) {
          recentlyViewed = JSON.parse(viewed);
        }
      }
    });
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
          Showing {totalProperties} premium homes
        </p>
      </div>
      <div class="flex gap-2 w-full md:w-auto flex-wrap">
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
          title="Toggle Filters"
        >
          <Filter class="w-4 h-4" />
        </Button>
        {#if $user}
          <Button
            variant="outline"
            size="icon"
            onclick={() => (isSaveSearchOpen = true)}
            title="Save Search"
          >
            <Save class="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            onclick={loadSavedSearches}
            title="My Saved Searches"
          >
            <History class="w-4 h-4" />
          </Button>
        {/if}
        <Select.Root
          type="single"
          bind:value={sortBy}
          onValueChange={handleSortChange}
        >
          <Select.Trigger class="w-[180px]">
            {sortBy === "newest"
              ? "Newest First"
              : sortBy === "price_asc"
                ? "Price: Low to High"
                : "Price: High to Low"}
          </Select.Trigger>
          <Select.Content>
            <Select.Item value="newest">Newest First</Select.Item>
            <Select.Item value="price_asc">Price: Low to High</Select.Item>
            <Select.Item value="price_desc">Price: High to Low</Select.Item>
          </Select.Content>
        </Select.Root>
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

    <!-- Pagination -->
    {#if totalPages > 1}
      <div class="flex justify-center items-center gap-2 mt-12">
        <Button
          variant="outline"
          size="sm"
          onclick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </Button>

        <div class="flex items-center gap-2 mx-4">
          <span class="text-sm text-muted-foreground">
            Page {currentPage} of {totalPages}
          </span>
        </div>

        <Button
          variant="outline"
          size="sm"
          onclick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>
      </div>
    {/if}
  {/if}

  {#if recentlyViewed.length > 0}
    <div class="mt-16">
      <h2 class="text-2xl font-bold mb-6">Recently Viewed</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each recentlyViewed as prop}
          <a href="/properties/{prop.id}" class="block group">
            <div
              class="border rounded-lg overflow-hidden hover:shadow-md transition-shadow"
            >
              <div class="h-40 overflow-hidden">
                <img
                  src={prop.image}
                  alt={prop.title}
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div class="p-4">
                <h4 class="font-semibold truncate">{prop.title}</h4>
                <p class="text-primary font-bold mt-1">₹ {prop.price}</p>
              </div>
            </div>
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>

<!-- Save Search Dialog -->
<Dialog.Root bind:open={isSaveSearchOpen}>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Save Search</Dialog.Title>
      <Dialog.Description>
        Give a name to your current search filters to access them easily later.
      </Dialog.Description>
    </Dialog.Header>
    <div class="py-4">
      <Label>Search Name</Label>
      <Input
        bind:value={searchName}
        placeholder="e.g. 3 BHK in Mumbai"
        class="mt-2"
      />
    </div>
    <Dialog.Footer>
      <Button onclick={saveSearch}>Save</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog.Root>

<!-- Saved Searches List Dialog -->
<Dialog.Root bind:open={isSavedSearchesListOpen}>
  <Dialog.Content class="max-w-md">
    <Dialog.Header>
      <Dialog.Title>My Saved Searches</Dialog.Title>
    </Dialog.Header>
    <div class="py-4 space-y-4 max-h-[60vh] overflow-y-auto">
      {#if savedSearches.length === 0}
        <p class="text-center text-muted-foreground">
          No saved searches found.
        </p>
      {:else}
        {#each savedSearches as search}
          <div
            class="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50"
          >
            <button
              class="flex-1 text-left"
              onclick={() => applySearch(search)}
            >
              <div class="font-medium">{search.name}</div>
              <div class="text-xs text-muted-foreground mt-1">
                {new Date(
                  search.createdAt.replace(" ", "T"),
                ).toLocaleDateString()}
              </div>
            </button>
            <Button
              variant="ghost"
              size="icon"
              class="text-red-500 hover:text-red-600 hover:bg-red-50"
              onclick={() => deleteSearch(search.id)}
            >
              <Trash2 class="w-4 h-4" />
            </Button>
          </div>
        {/each}
      {/if}
    </div>
  </Dialog.Content>
</Dialog.Root>
