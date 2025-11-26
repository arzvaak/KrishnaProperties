<script lang="ts">
  import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
  } from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";
  import { Badge } from "$lib/components/ui/badge";
  import { MapPin, Bed, Bath, Square, Heart } from "lucide-svelte";
  import { user } from "$lib/stores/auth";
  import { toast } from "svelte-sonner";

  export let property: any;
  let isFavorite = false; // In a real app, check this against user's favorites list on mount

  async function toggleFavorite(e: Event) {
    e.preventDefault();
    e.stopPropagation();

    if (!$user) {
      toast.error("Please login to save properties");
      return;
    }

    try {
      const method = isFavorite ? "DELETE" : "POST";
      const url = isFavorite
        ? `http://127.0.0.1:5000/api/users/${$user.uid}/favorites/${property.id}`
        : `http://127.0.0.1:5000/api/users/${$user.uid}/favorites`;

      const body = isFavorite
        ? undefined
        : JSON.stringify({ propertyId: property.id });

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body,
      });

      if (!response.ok) throw new Error("Failed to update favorites");

      isFavorite = !isFavorite;
      toast.success(
        isFavorite ? "Added to favorites" : "Removed from favorites",
      );
    } catch (error: any) {
      toast.error(error.message);
    }
  }
</script>

<Card class="overflow-hidden hover:shadow-lg transition-shadow group relative">
  <div class="relative h-48 overflow-hidden">
    <img
      src={property.imageUrl ||
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
      alt={property.title}
      class="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
    />
    <div class="absolute top-2 left-2 flex gap-2">
      <Badge variant="secondary" class="bg-background/80 backdrop-blur-sm">
        {property.type}
      </Badge>
    </div>
    <Button
      variant="ghost"
      size="icon"
      class="absolute top-2 right-2 bg-background/80 backdrop-blur-sm hover:bg-background/90 text-foreground"
      onclick={toggleFavorite}
    >
      <Heart class="h-5 w-5 {isFavorite ? 'fill-red-500 text-red-500' : ''}" />
    </Button>
  </div>

  <CardHeader class="p-4 pb-0">
    <h3 class="font-bold text-lg line-clamp-1">{property.title}</h3>
    <div class="flex items-center text-muted-foreground text-sm mt-1">
      <MapPin class="w-4 h-4 mr-1" />
      <span class="line-clamp-1">{property.location}</span>
    </div>
  </CardHeader>

  <CardContent class="p-4">
    <div class="flex justify-between items-center mb-4">
      <span class="text-xl font-bold text-primary">₹ {property.price}</span>
    </div>

    <div
      class="grid grid-cols-3 gap-2 text-sm text-muted-foreground border-t pt-4"
    >
      <div class="flex items-center gap-1">
        <Bed class="w-4 h-4" />
        <span>{property.bedrooms} Beds</span>
      </div>
      <div class="flex items-center gap-1">
        <Bath class="w-4 h-4" />
        <span>{property.bathrooms} Baths</span>
      </div>
      <div class="flex items-center gap-1">
        <Square class="w-4 h-4" />
        <span>{property.area} sqft</span>
      </div>
    </div>
  </CardContent>

  <CardFooter class="p-4 pt-0">
    <Button variant="outline" class="w-full" href="/properties/{property.id}">
      View Details
    </Button>
  </CardFooter>
</Card>
