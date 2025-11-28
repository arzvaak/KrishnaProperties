<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import {
        Plus,
        Trash2,
        School,
        Hospital,
        Bus,
        ShoppingBag,
        Utensils,
    } from "lucide-svelte";

    export let amenities: { name: string; type: string; distance: string }[] =
        [];

    const amenityTypes = [
        { value: "School", label: "School", icon: School },
        { value: "Hospital", label: "Hospital", icon: Hospital },
        { value: "Transport", label: "Transport", icon: Bus },
        { value: "Shopping", label: "Shopping", icon: ShoppingBag },
        { value: "Restaurant", label: "Restaurant", icon: Utensils },
        { value: "Other", label: "Other", icon: Plus },
    ];

    function addAmenity() {
        amenities = [...amenities, { name: "", type: "School", distance: "" }];
    }

    function removeAmenity(index: number) {
        amenities = amenities.filter((_, i) => i !== index);
    }
</script>

<div class="space-y-4">
    <div class="flex items-center justify-between">
        <Label>Nearby Amenities</Label>
        <Button variant="outline" size="sm" onclick={addAmenity} type="button">
            <Plus class="w-4 h-4 mr-2" /> Add Amenity
        </Button>
    </div>

    {#if amenities.length === 0}
        <div
            class="text-sm text-muted-foreground text-center py-4 border rounded-md border-dashed"
        >
            No amenities added yet.
        </div>
    {:else}
        <div class="space-y-3">
            {#each amenities as amenity, i}
                <div class="grid grid-cols-12 gap-2 items-end">
                    <div class="col-span-4 space-y-1">
                        <Label class="text-xs">Name</Label>
                        <Input
                            bind:value={amenity.name}
                            placeholder="e.g. St. Mary's School"
                        />
                    </div>
                    <div class="col-span-4 space-y-1">
                        <Label class="text-xs">Type</Label>
                        <select
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                            bind:value={amenity.type}
                        >
                            {#each amenityTypes as type}
                                <option value={type.value}>{type.label}</option>
                            {/each}
                        </select>
                    </div>
                    <div class="col-span-3 space-y-1">
                        <Label class="text-xs">Distance (km)</Label>
                        <Input
                            bind:value={amenity.distance}
                            placeholder="e.g. 1.2"
                        />
                    </div>
                    <div class="col-span-1">
                        <Button
                            variant="ghost"
                            size="icon"
                            class="text-destructive hover:bg-destructive/10"
                            onclick={() => removeAmenity(i)}
                            type="button"
                        >
                            <Trash2 class="w-4 h-4" />
                        </Button>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>
