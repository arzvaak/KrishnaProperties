<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "$lib/components/ui/table";
  import { toast } from "svelte-sonner";
  import { LayoutGrid, List, Pencil, Trash2 } from "lucide-svelte";
  import PropertyCard from "$lib/components/PropertyCard.svelte";

  let properties: any[] = [];
  let loading = true;
  let viewMode: "list" | "grid" = "grid"; // Default to grid as requested

  async function fetchProperties() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/properties");
      if (!response.ok) throw new Error("Failed to fetch properties");
      const data = await response.json();
      properties = data.properties || [];
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      loading = false;
    }
  }

  async function deleteProperty(id: string) {
    if (!confirm("Are you sure you want to delete this property?")) return;
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/properties/${id}`,
        {
          method: "DELETE",
        },
      );
      if (!response.ok) throw new Error("Failed to delete property");
      toast.success("Property deleted successfully");
      fetchProperties();
    } catch (error: any) {
      toast.error(error.message);
    }
  }

  onMount(fetchProperties);
</script>

<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold">Manage Properties</h1>
  <div class="flex items-center gap-4">
    <div class="flex items-center gap-2 bg-muted p-1 rounded-lg">
      <Button
        variant={viewMode === "list" ? "secondary" : "ghost"}
        size="sm"
        onclick={() => (viewMode = "list")}
      >
        <List class="w-4 h-4" />
      </Button>
      <Button
        variant={viewMode === "grid" ? "secondary" : "ghost"}
        size="sm"
        onclick={() => (viewMode = "grid")}
      >
        <LayoutGrid class="w-4 h-4" />
      </Button>
    </div>
    <Button href="/admin/properties/add">Add New Property</Button>
  </div>
</div>

{#if loading}
  <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
    {#each Array(6) as _}
      <div class="h-[400px] bg-muted rounded-xl animate-pulse"></div>
    {/each}
  </div>
{:else if properties.length === 0}
  <div class="text-center py-12 border rounded-lg bg-muted/10">
    <h3 class="text-lg font-medium">No properties found</h3>
    <p class="text-muted-foreground">Add your first property to get started.</p>
  </div>
{:else if viewMode === "grid"}
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
    {#each properties as property}
      <PropertyCard {property} adminMode={true} onDelete={deleteProperty} />
    {/each}
  </div>
{:else}
  <div class="rounded-md border">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Title</TableHead>
          <TableHead>Location</TableHead>
          <TableHead>Price</TableHead>
          <TableHead>Type</TableHead>
          <TableHead class="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {#each properties as property}
          <TableRow>
            <TableCell class="font-medium">{property.title}</TableCell>
            <TableCell>{property.location}</TableCell>
            <TableCell>₹ {property.price}</TableCell>
            <TableCell>{property.type}</TableCell>
            <TableCell class="text-right">
              <Button
                variant="ghost"
                size="icon"
                class="mr-2"
                href={`/admin/properties/${property.id}/edit`}
              >
                <Pencil class="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                class="text-red-500 hover:text-red-600"
                onclick={() => deleteProperty(property.id)}
              >
                <Trash2 class="h-4 w-4" />
              </Button>
            </TableCell>
          </TableRow>
        {/each}
      </TableBody>
    </Table>
  </div>
{/if}
