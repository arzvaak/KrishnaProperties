<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { user } from "$lib/stores/auth";
  import { Button } from "$lib/components/ui/button";
  import { Badge } from "$lib/components/ui/badge";
  import { Card, CardContent } from "$lib/components/ui/card";
  import {
    MapPin,
    Bed,
    Bath,
    Square,
    Calendar,
    Phone,
    Mail,
    ChevronLeft,
    ChevronRight,
    Heart,
    Share2,
  } from "lucide-svelte";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import { toast } from "svelte-sonner";
  import emblaCarouselSvelte from "embla-carousel-svelte";
  import Autoplay from "embla-carousel-autoplay";
  import Map from "$lib/components/Map.svelte";

  let property: any = null;
  let similarProperties: any[] = [];
  let loading = true;
  let error: string | null = null;
  const id = $page.params.id;
  let emblaApi: any;

  let message = "";
  let contactSent = false;
  let isFavorite = false;

  async function toggleFavorite() {
    if (!$user) {
      toast.error("Please login to save properties");
      return;
    }

    try {
      const method = isFavorite ? "DELETE" : "POST";
      const url = isFavorite
        ? `http://127.0.0.1:5000/api/users/${$user.uid}/favorites/${id}`
        : `http://127.0.0.1:5000/api/users/${$user.uid}/favorites`;

      const body = isFavorite ? undefined : JSON.stringify({ propertyId: id });

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

  function getEmbedUrl(url: string) {
    if (!url) return null;

    // YouTube
    const ytMatch = url.match(
      /(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^#&?]*).*/,
    );
    if (ytMatch && ytMatch[1])
      return `https://www.youtube.com/embed/${ytMatch[1]}`;

    // Vimeo
    const vimeoMatch = url.match(/(?:vimeo\.com\/)([0-9]+)/);
    if (vimeoMatch && vimeoMatch[1])
      return `https://player.vimeo.com/video/${vimeoMatch[1]}`;

    return null;
  }

  async function handleContact() {
    try {
      await fetch("http://127.0.0.1:5000/api/analytics/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "contact",
          property_id: id,
          metadata: { message },
        }),
      });
      contactSent = true;
      toast.success("Message sent to agent!");
      message = "";
    } catch (e) {
      toast.error("Failed to send message");
    }
  }

  onMount(async () => {
    try {
      // Track property view
      fetch("http://127.0.0.1:5000/api/analytics/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "property_view", property_id: id }),
      }).catch(console.error);

      const [propResponse, allPropsResponse] = await Promise.all([
        fetch(`http://127.0.0.1:5000/api/properties/${id}`),
        fetch(`http://127.0.0.1:5000/api/properties/${id}`),
        fetch(`http://127.0.0.1:5000/api/properties`),
      ]);

      // Check if favorite
      user.subscribe(async (u) => {
        if (u) {
          try {
            const res = await fetch(
              `http://127.0.0.1:5000/api/users/${u.uid}/favorites`,
            );
            if (res.ok) {
              const favs = await res.json();
              isFavorite = favs.some((f: any) => f.id === id);
            }
          } catch (e) {
            console.error("Failed to check favorite status");
          }
        }
      });

      if (!propResponse.ok) throw new Error("Failed to fetch property details");
      property = await propResponse.json();

      if (allPropsResponse.ok) {
        const allProps = await allPropsResponse.json();
        // Filter out current property and take 3 random ones (or just next 3)
        similarProperties = allProps
          .filter((p: any) => p.id !== id)
          .slice(0, 3);
      }
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });
</script>

<div class="container py-8">
  {#if loading}
    <div class="space-y-8">
      <Skeleton class="h-[400px] w-full rounded-xl" />
      <div class="space-y-4">
        <Skeleton class="h-8 w-[300px]" />
        <Skeleton class="h-4 w-full" />
        <Skeleton class="h-4 w-full" />
      </div>
    </div>
  {:else if error}
    <div class="text-center py-20 text-red-500">
      <p>Error: {error}</p>
      <Button variant="outline" class="mt-4" href="/properties"
        >Back to Properties</Button
      >
    </div>
  {:else if property}
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Content -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Image Carousel -->
        <div class="relative group">
          <div
            class="overflow-hidden rounded-xl bg-muted"
            use:emblaCarouselSvelte={{
              options: { loop: true },
              plugins: [Autoplay({ delay: 5000 })],
            }}
            onemblaInit={(event) => (emblaApi = event.detail)}
          >
            <div class="flex">
              {#if property.images && property.images.length > 0}
                {#each property.images as image}
                  <div class="flex-[0_0_100%] min-w-0 relative h-[500px]">
                    <img
                      src={image}
                      alt={property.title}
                      class="object-cover w-full h-full"
                    />
                  </div>
                {/each}
              {:else}
                <div class="flex-[0_0_100%] min-w-0 relative h-[500px]">
                  <img
                    src={property.imageUrl ||
                      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
                    alt={property.title}
                    class="object-cover w-full h-full"
                  />
                </div>
              {/if}

              <!-- Video Slide -->
              {#if property.videoUrl}
                <div
                  class="flex-[0_0_100%] min-w-0 relative h-[500px] bg-black flex items-center justify-center"
                >
                  {#if property.videoType === "file" || !getEmbedUrl(property.videoUrl)}
                    <video
                      src={property.videoUrl}
                      controls
                      class="w-full h-full max-h-[500px]"
                    >
                      <track kind="captions" />
                    </video>
                  {:else}
                    <iframe
                      src={getEmbedUrl(property.videoUrl)}
                      title="Property Video"
                      class="w-full h-full"
                      frameborder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowfullscreen
                    ></iframe>
                  {/if}
                </div>
              {/if}
            </div>
          </div>

          <!-- Navigation Buttons -->
          <button
            class="absolute left-4 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-black/50 text-white backdrop-blur-sm border border-white/10 hover:bg-black/70 transition-all opacity-0 group-hover:opacity-100"
            onclick={() => emblaApi && emblaApi.scrollPrev()}
          >
            <ChevronLeft class="w-6 h-6" />
          </button>
          <button
            class="absolute right-4 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-black/50 text-white backdrop-blur-sm border border-white/10 hover:bg-black/70 transition-all opacity-0 group-hover:opacity-100"
            onclick={() => emblaApi && emblaApi.scrollNext()}
          >
            <ChevronRight class="w-6 h-6" />
          </button>
        </div>

        <div>
          <div class="flex justify-between items-start mb-2">
            <h1 class="text-3xl font-bold">{property.title}</h1>
            <div class="flex gap-2">
              <Button variant="outline" size="icon" onclick={toggleFavorite}>
                <Heart
                  class="w-5 h-5 {isFavorite
                    ? 'fill-red-500 text-red-500'
                    : ''}"
                />
              </Button>
              <Button variant="outline" size="icon">
                <Share2 class="w-5 h-5" />
              </Button>
            </div>
          </div>
          <div class="flex items-center text-muted-foreground mb-4">
            <MapPin class="w-5 h-5 mr-2" />
            <span class="text-lg">{property.location}</span>
          </div>
          <p class="text-2xl font-bold text-primary mb-6">₹ {property.price}</p>

          <div
            class="grid grid-cols-3 gap-4 p-6 bg-card border rounded-lg mb-8"
          >
            <div class="flex flex-col items-center justify-center text-center">
              <Bed class="w-6 h-6 mb-2 text-primary" />
              <span class="font-bold">{property.bedrooms}</span>
              <span class="text-xs text-muted-foreground">Bedrooms</span>
            </div>
            <div
              class="flex flex-col items-center justify-center text-center border-x"
            >
              <Bath class="w-6 h-6 mb-2 text-primary" />
              <span class="font-bold">{property.bathrooms}</span>
              <span class="text-xs text-muted-foreground">Bathrooms</span>
            </div>
            <div class="flex flex-col items-center justify-center text-center">
              <Square class="w-6 h-6 mb-2 text-primary" />
              <span class="font-bold">{property.sqft || "N/A"}</span>
              <span class="text-xs text-muted-foreground">Sq Ft</span>
            </div>
          </div>

          <div class="prose max-w-none mb-8">
            <h3 class="text-xl font-bold mb-4">Description</h3>
            <p class="text-muted-foreground">
              {property.description ||
                "No description available for this property."}
            </p>
          </div>

          <!-- Map Section -->
          <div class="h-[400px] rounded-xl overflow-hidden border">
            <Map
              lat={property.lat || 19.076}
              lng={property.lng || 72.8777}
              zoom={15}
            />
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <Card>
          <CardContent class="p-6 space-y-4">
            <h3 class="font-bold text-lg">Contact Us</h3>
            <p class="text-sm text-muted-foreground">
              Interested in this property? Send us a message and we'll get back
              to you shortly.
            </p>
            <div class="space-y-3">
              {#if contactSent}
                <div
                  class="bg-green-50 text-green-700 p-4 rounded-lg text-sm text-center"
                >
                  Message sent successfully! The agent will contact you shortly.
                </div>
              {:else}
                <textarea
                  class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="I'm interested in this property..."
                  bind:value={message}
                ></textarea>
                <Button
                  class="w-full gap-2"
                  onclick={handleContact}
                  disabled={!message}
                >
                  <Mail class="w-4 h-4" /> Send Message
                </Button>
              {/if}
              <Button
                variant="outline"
                class="w-full gap-2"
                href="tel:+919876543210"
              >
                <Phone class="w-4 h-4" /> Call Us
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent class="p-6">
            <h3 class="font-bold text-lg mb-4">Mortgage Calculator</h3>
            <p class="text-sm text-muted-foreground mb-4">
              Estimated monthly payment based on 20% down payment and 8.5%
              interest rate.
            </p>
            <div class="text-2xl font-bold text-primary">
              ₹ {Math.round(
                parseInt(property.price.replace(/[^0-9]/g, "")) * 0.0076,
              )} / mo
            </div>
          </CardContent>
        </Card>

        {#if similarProperties.length > 0}
          <div class="space-y-4">
            <h3 class="font-bold text-lg">You Might Also Like</h3>
            {#each similarProperties as prop}
              <a href="/properties/{prop.id}" class="block group">
                <Card class="overflow-hidden hover:shadow-md transition-shadow">
                  <div class="flex gap-3 p-3">
                    <div
                      class="w-24 h-24 rounded-lg overflow-hidden flex-shrink-0"
                    >
                      <img
                        src={prop.imageUrl ||
                          prop.images?.[0] ||
                          "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
                        alt={prop.title}
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                    <div class="flex flex-col justify-between py-1">
                      <div>
                        <h4
                          class="font-semibold text-sm line-clamp-2 group-hover:text-primary transition-colors"
                        >
                          {prop.title}
                        </h4>
                        <p class="text-xs text-muted-foreground mt-1">
                          {prop.location}
                        </p>
                      </div>
                      <p class="font-bold text-primary text-sm">
                        ₹ {prop.price}
                      </p>
                    </div>
                  </div>
                </Card>
              </a>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {/if}
</div>
