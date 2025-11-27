<script lang="ts">
  import { onMount } from "svelte";
  import PropertyCard from "$lib/components/PropertyCard.svelte";
  import PropertyFilters from "$lib/components/PropertyFilters.svelte";
  import { Button } from "$lib/components/ui/button";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import * as Select from "$lib/components/ui/select";
  import { Filter, Trash2 } from "lucide-svelte";
  import { fade } from "svelte/transition";
  import { user } from "$lib/stores/auth";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import { toast } from "svelte-sonner";
  import { reveal } from "$lib/actions/reveal";

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

<div class="flex flex-col min-h-screen bg-background">
  <!-- Page Header -->
  <section
    class="relative h-[400px] flex items-center justify-center overflow-hidden"
  >
    <div class="absolute inset-0">
      <img
        src="/images/interior-bg.png"
        alt="Properties"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-black/60 backdrop-blur-[2px]"></div>
    </div>
    <div class="relative z-10 container px-4 text-center" use:reveal>
      <h1 class="text-5xl font-bold text-white mb-4 tracking-tight">
        Premium Listings
      </h1>
      <p class="text-xl text-gray-200 max-w-2xl mx-auto font-light">
        Explore our curated collection of exclusive properties.
      </p>
    </div>
  </section>

  <div class="container py-12 -mt-20 relative z-20">
    <!-- Search & Filter Bar -->
    <PropertyFilters
      bind:searchQuery
      bind:minPrice
      bind:maxPrice
      bind:bedrooms
      bind:propertyType
      bind:showFilters
      onSearch={fetchProperties}
      onClear={clearFilters}
      onSaveSearch={() => (isSaveSearchOpen = true)}
      onLoadSavedSearches={loadSavedSearches}
    />

    <!-- Results Header -->
    <div class="flex justify-between items-center mb-8">
      <p class="text-muted-foreground text-lg">
        Found <span class="font-bold text-foreground">{totalProperties}</span> properties
      </p>
      <Select.Root
        type="single"
        bind:value={sortBy}
        onValueChange={handleSortChange}
      >
        <Select.Trigger class="w-[200px]">
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

    <!-- Property Grid -->
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
      <div
        class="text-center py-32 bg-muted/30 rounded-3xl border border-dashed"
      >
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
        <div class="flex justify-center items-center gap-4 mt-16">
          <Button
            variant="outline"
            onclick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </Button>

          <div class="flex items-center gap-2">
            {#each Array(totalPages) as _, i}
              <button
                class="w-10 h-10 rounded-full flex items-center justify-center transition-colors {currentPage ===
                i + 1
                  ? 'bg-primary text-primary-foreground font-bold'
                  : 'hover:bg-muted'}"
                onclick={() => handlePageChange(i + 1)}
              >
                {i + 1}
              </button>
            {/each}
          </div>

          <Button
            variant="outline"
            onclick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </Button>
        </div>
      {/if}
    {/if}

    <!-- Recently Viewed -->
    {#if recentlyViewed.length > 0}
      <div class="mt-24 pt-12 border-t border-border/50">
        <h2 class="text-2xl font-bold mb-8">Recently Viewed</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {#each recentlyViewed as prop}
            <a href="/properties/{prop.id}" class="block group">
              <div
                class="border rounded-xl overflow-hidden hover:shadow-lg transition-all duration-300 bg-card"
              >
                <div class="h-48 overflow-hidden relative">
                  <img
                    src={prop.image}
                    alt={prop.title}
                    class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div
                    class="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors"
                  ></div>
                </div>
                <div class="p-4">
                  <h4 class="font-semibold truncate text-lg">{prop.title}</h4>
                  <p class="text-primary font-bold mt-1">₹ {prop.price}</p>
                </div>
              </div>
            </a>
          {/each}
        </div>
      </div>
    {/if}
  </div>
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
