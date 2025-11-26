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
  import { Pencil, Trash2 } from "lucide-svelte";

  let properties: any[] = [];
  let loading = true;

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
  <Button href="/admin/properties/add">Add New Property</Button>
</div>

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
      {#if loading}
        <TableRow>
          <TableCell colspan={5} class="text-center py-8">Loading...</TableCell>
        </TableRow>
      {:else if properties.length === 0}
        <TableRow>
          <TableCell colspan={5} class="text-center py-8"
            >No properties found.</TableCell
          >
        </TableRow>
      {:else}
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
      {/if}
    </TableBody>
  </Table>
</div>
