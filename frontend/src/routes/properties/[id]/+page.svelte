<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
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
  } from "lucide-svelte";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import { toast } from "svelte-sonner";
  import emblaCarouselSvelte from "embla-carousel-svelte";
  import Autoplay from "embla-carousel-autoplay";
  import Map from "$lib/components/Map.svelte";

  let property: any = null;
  let loading = true;
  let error = null;
  const id = $page.params.id;
  let emblaApi: any;

  let message = "";
  let contactSent = false;

  function handleContact() {
    // Simulate API call
    setTimeout(() => {
      contactSent = true;
      toast.success("Message sent to agent!");
      message = "";
    }, 1000);
  }

  onMount(async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/properties/${id}`,
      );
      if (!response.ok) throw new Error("Failed to fetch property details");
      property = await response.json();
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
          <h1 class="text-3xl font-bold mb-2">{property.title}</h1>
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
            <h3 class="font-bold text-lg">Contact Agent</h3>
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-full bg-muted overflow-hidden">
                <img
                  src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                  alt="Agent"
                />
              </div>
              <div>
                <p class="font-medium">Rahul Sharma</p>
                <p class="text-xs text-muted-foreground">Senior Agent</p>
              </div>
            </div>
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
                <Phone class="w-4 h-4" /> Call Agent
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
      </div>
    </div>
  {/if}
</div>
