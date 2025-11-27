<script lang="ts">
  import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
  } from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";
  import { Badge } from "$lib/components/ui/badge";
  import { MapPin, Bed, Bath, Maximize, Heart } from "lucide-svelte";
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

<a href="/properties/{property.id}" class="block group h-full">
  <Card
    class="h-full relative overflow-hidden border-border/50 shadow-lg hover:shadow-2xl transition-all duration-500 bg-card/80 backdrop-blur-sm hover:-translate-y-2"
  >
    <div class="relative aspect-[4/3] overflow-hidden rounded-t-xl">
      <img
        src={property.imageUrl ||
          property.images?.[0] ||
          "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
        alt={property.title}
        class="object-cover w-full h-full group-hover:scale-110 transition-transform duration-700"
      />
      <div
        class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-300"
      ></div>

      <div class="absolute top-3 left-3 flex gap-2 z-10">
        <Badge
          class="bg-white/90 text-black backdrop-blur-md hover:bg-white border-none shadow-sm"
        >
          {property.type}
        </Badge>
      </div>

      <Button
        variant="ghost"
        size="icon"
        class="absolute top-3 right-3 z-10 rounded-full bg-white/20 backdrop-blur-md hover:bg-white text-white hover:text-red-500 transition-all duration-300"
        onclick={toggleFavorite}
      >
        <Heart
          class="h-5 w-5 {isFavorite ? 'fill-red-500 text-red-500' : ''}"
        />
      </Button>

      <div
        class="absolute bottom-4 left-4 right-4 translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-300 z-10"
      >
        <span
          class="inline-flex items-center justify-center w-full py-2 bg-primary text-primary-foreground font-medium rounded-lg shadow-lg"
        >
          View Details
        </span>
      </div>
    </div>

    <CardContent class="p-5">
      <div class="flex justify-between items-start mb-3">
        <div>
          <h3
            class="font-bold text-xl text-foreground group-hover:text-primary transition-colors line-clamp-1"
          >
            {property.title}
          </h3>
          <div class="flex items-center text-muted-foreground text-sm mt-1">
            <MapPin class="w-3.5 h-3.5 mr-1" />
            <span class="line-clamp-1">{property.location}</span>
          </div>
        </div>
        <div class="text-right">
          <span class="text-lg font-bold text-primary block"
            >₹ {property.price}</span
          >
        </div>
      </div>

      <div class="grid grid-cols-3 gap-4 py-4 border-t border-border/50 mt-4">
        <div
          class="flex flex-col items-center justify-center p-2 rounded-lg bg-muted/30"
        >
          <Bed class="w-5 h-5 mb-1 text-primary/80" />
          <span class="text-xs font-medium text-muted-foreground"
            >{property.bedrooms} Beds</span
          >
        </div>
        <div
          class="flex flex-col items-center justify-center p-2 rounded-lg bg-muted/30"
        >
          <Bath class="w-5 h-5 mb-1 text-primary/80" />
          <span class="text-xs font-medium text-muted-foreground"
            >{property.bathrooms} Baths</span
          >
        </div>
        <div
          class="flex flex-col items-center justify-center p-2 rounded-lg bg-muted/30"
        >
          <Maximize class="w-5 h-5 mb-1 text-primary/80" />
          <span class="text-xs font-medium text-muted-foreground"
            >{property.area} sqft</span
          >
        </div>
      </div>
    </CardContent>
  </Card>
</a>
