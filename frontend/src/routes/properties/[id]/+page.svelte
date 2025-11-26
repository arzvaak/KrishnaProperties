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
    Phone,
    Mail,
    ChevronLeft,
    ChevronRight,
    Heart,
    Share2,
    Printer,
    Copy,
    Facebook,
    Twitter,
    Calendar as CalendarIcon,
  } from "lucide-svelte";
  import * as Dialog from "$lib/components/ui/dialog";
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
  let isShareOpen = false;

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

  function handleShare() {
    isShareOpen = true;
  }

  function copyLink() {
    navigator.clipboard.writeText(window.location.href);
    toast.success("Link copied to clipboard!");
    isShareOpen = false;
  }

  function shareSocial(platform: string) {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(
      `Check out this property: ${property.title}`,
    );
    let shareUrl = "";

    switch (platform) {
      case "whatsapp":
        shareUrl = `https://wa.me/?text=${text}%20${url}`;
        break;
      case "facebook":
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
        break;
      case "twitter":
        shareUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
        break;
      case "email":
        shareUrl = `mailto:?subject=${text}&body=${url}`;
        break;
    }

    if (shareUrl) {
      window.open(shareUrl, "_blank");
      isShareOpen = false;
    }
  }

  function handlePrint() {
    window.print();
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

  import { Calendar } from "$lib/components/ui/calendar";
  import * as Popover from "$lib/components/ui/popover";
  import { cn } from "$lib/utils";
  import {
    DateFormatter,
    type DateValue,
    getLocalTimeZone,
  } from "@internationalized/date";

  let date: DateValue | undefined = undefined;
  let time = "10:00";
  let isScheduleOpen = false;
  let scheduling = false;
  let selectedIndex = 0;

  const df = new DateFormatter("en-US", {
    dateStyle: "long",
  });

  async function handleContact() {
    try {
      await fetch("http://127.0.0.1:5000/api/analytics/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "contact",
          property_id: id,
          user_id: $user?.uid,
          metadata: { message },
        }),
      });
      contactSent = true;
      toast.success("Message sent to team!");
      message = "";
    } catch (e) {
      toast.error("Failed to send message");
    }
  }

  async function handleSchedule() {
    if (!$user) {
      toast.error("Please login to schedule a viewing");
      return;
    }
    if (!date) {
      toast.error("Please select a date");
      return;
    }

    scheduling = true;
    try {
      const res = await fetch("http://127.0.0.1:5000/api/appointments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: $user.uid,
          property_id: id,
          date: date.toString(),
          time: time,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to schedule");

      toast.success(data.message);
      isScheduleOpen = false;
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      scheduling = false;
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

      // Save to recently viewed
      user.subscribe(async (u) => {
        if (u) {
          // Logged in: Save to API
          try {
            await fetch(
              `http://127.0.0.1:5000/api/users/${u.uid}/recently-viewed`,
              {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ propertyId: property.id }),
              },
            );
          } catch (e) {
            console.error("Failed to save recently viewed to API", e);
          }
        } else {
          // Guest: Save to localStorage
          const viewed = localStorage.getItem("recentlyViewed");
          let recentlyViewed = viewed ? JSON.parse(viewed) : [];
          recentlyViewed = recentlyViewed.filter(
            (p: any) => p.id !== property.id,
          );
          recentlyViewed.unshift({
            id: property.id,
            title: property.title,
            price: property.price,
            image:
              property.images?.[0] ||
              property.imageUrl ||
              "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
          });
          if (recentlyViewed.length > 4) recentlyViewed.pop();
          localStorage.setItem(
            "recentlyViewed",
            JSON.stringify(recentlyViewed),
          );
        }
      });

      if (allPropsResponse.ok) {
        const data = await allPropsResponse.json();
        const allProps = data.properties || [];
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
            onemblaInit={(event) => {
              emblaApi = event.detail;
              emblaApi.on("select", () => {
                selectedIndex = emblaApi.selectedScrollSnap();
              });
            }}
          >
            <div class="flex">
              {#if property.images && property.images.length > 0}
                {#each property.images as image}
                  <div class="flex-[0_0_100%] min-w-0 relative h-[500px]">
                    <img
                      src={image}
                      alt={property.title}
                      class="object-cover w-full h-full"
                      onerror={(e) => {
                        const img = e.currentTarget as HTMLImageElement;
                        img.onerror = null;
                        img.src =
                          "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80";
                      }}
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
                    onerror={(e) => {
                      const img = e.currentTarget as HTMLImageElement;
                      img.onerror = null;
                      img.src =
                        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80";
                    }}
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

        <!-- Thumbnails -->
        {#if property.images && property.images.length > 0}
          <div class="flex gap-2 overflow-x-auto pb-2">
            {#each property.images as image, i}
              <button
                class="relative w-24 h-16 flex-shrink-0 rounded-md overflow-hidden border-2 transition-all {i ===
                selectedIndex
                  ? 'border-primary ring-2 ring-primary/50'
                  : 'border-transparent opacity-70 hover:opacity-100'}"
                onclick={() => emblaApi && emblaApi.scrollTo(i)}
              >
                <img
                  src={image}
                  alt={`Thumbnail ${i + 1}`}
                  class="object-cover w-full h-full"
                />
              </button>
            {/each}
            {#if property.videoUrl}
              <button
                class="relative w-24 h-16 flex-shrink-0 rounded-md overflow-hidden border-2 transition-all {property
                  .images.length === selectedIndex
                  ? 'border-primary ring-2 ring-primary/50'
                  : 'border-transparent opacity-70 hover:opacity-100'}"
                onclick={() =>
                  emblaApi && emblaApi.scrollTo(property.images.length)}
              >
                <div
                  class="w-full h-full bg-black flex items-center justify-center text-white"
                >
                  <span class="text-xs">Video</span>
                </div>
              </button>
            {/if}
          </div>
        {/if}

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
              <Button
                variant="outline"
                size="icon"
                onclick={handleShare}
                class="no-print"
              >
                <Share2 class="w-5 h-5" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                onclick={handlePrint}
                class="no-print"
              >
                <Printer class="w-5 h-5" />
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
              <Popover.Root bind:open={isScheduleOpen}>
                <Popover.Trigger class="w-full">
                  <Button variant="outline" class="w-full gap-2">
                    <CalendarIcon class="w-4 h-4" /> Schedule Viewing
                  </Button>
                </Popover.Trigger>
                <Popover.Content class="w-auto p-0" align="start">
                  <div class="p-4 space-y-4">
                    <div class="space-y-2">
                      <h4 class="font-medium leading-none">Pick a date</h4>
                      <Calendar
                        bind:value={date}
                        type="single"
                        class="rounded-md border"
                      />
                    </div>
                    <div class="space-y-2">
                      <h4 class="font-medium leading-none">Pick a time</h4>
                      <select
                        bind:value={time}
                        class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        <option value="10:00">10:00 AM</option>
                        <option value="11:00">11:00 AM</option>
                        <option value="12:00">12:00 PM</option>
                        <option value="13:00">01:00 PM</option>
                        <option value="14:00">02:00 PM</option>
                        <option value="15:00">03:00 PM</option>
                        <option value="16:00">04:00 PM</option>
                        <option value="17:00">05:00 PM</option>
                      </select>
                    </div>
                    <Button
                      class="w-full"
                      onclick={handleSchedule}
                      disabled={scheduling}
                    >
                      {scheduling ? "Scheduling..." : "Confirm Booking"}
                    </Button>
                  </div>
                </Popover.Content>
              </Popover.Root>
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

<Dialog.Root bind:open={isShareOpen}>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Share Property</Dialog.Title>
      <Dialog.Description>
        Share this property with your friends and family.
      </Dialog.Description>
    </Dialog.Header>
    <div class="grid grid-cols-2 gap-4 py-4">
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2"
        onclick={() => shareSocial("whatsapp")}
      >
        <span class="text-2xl">📱</span>
        WhatsApp
      </Button>
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2"
        onclick={() => shareSocial("facebook")}
      >
        <Facebook class="w-6 h-6 text-blue-600" />
        Facebook
      </Button>
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2"
        onclick={() => shareSocial("twitter")}
      >
        <Twitter class="w-6 h-6 text-sky-500" />
        Twitter
      </Button>
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2"
        onclick={() => shareSocial("email")}
      >
        <Mail class="w-6 h-6" />
        Email
      </Button>
    </div>
    <div class="flex items-center space-x-2">
      <div class="grid flex-1 gap-2">
        <Button
          variant="secondary"
          class="w-full justify-start text-muted-foreground"
          onclick={copyLink}
        >
          <Copy class="mr-2 h-4 w-4" />
          Copy Link
        </Button>
      </div>
    </div>
  </Dialog.Content>
</Dialog.Root>

<style>
  @media print {
    :global(body > *:not(.container)),
    :global(nav),
    :global(footer) {
      display: none !important;
    }

    :global(body) {
      background: white;
    }

    .container {
      max-width: 100% !important;
      padding: 0 !important;
      margin: 0 !important;
    }

    /* Hide carousel navigation */
    :global(.embla__button) {
      display: none !important;
    }
  }
</style>
