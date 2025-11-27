<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { user } from "$lib/stores/auth";
  import { Button } from "$lib/components/ui/button";
  import { Badge } from "$lib/components/ui/badge";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Separator } from "$lib/components/ui/separator";
  import {
    MapPin,
    Bed,
    Bath,
    Maximize,
    Heart,
    Share2,
    Printer,
    Copy,
    Facebook,
    Twitter,
    Mail,
  } from "lucide-svelte";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import { toast } from "svelte-sonner";
  import Map from "$lib/components/Map.svelte";
  import ImageGallery from "$lib/components/ImageGallery.svelte";
  import ContactAgentForm from "$lib/components/ContactAgentForm.svelte";
  import MortgageCalculator from "$lib/components/MortgageCalculator.svelte";

  let property: any = null;
  let similarProperties: any[] = [];
  let loading = true;
  let error: string | null = null;
  const id = $page.params.id;

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
    const ytMatch = url.match(
      /(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^#&?]*).*/,
    );
    if (ytMatch && ytMatch[1])
      return `https://www.youtube.com/embed/${ytMatch[1]}`;
    const vimeoMatch = url.match(/(?:vimeo\.com\/)([0-9]+)/);
    if (vimeoMatch && vimeoMatch[1])
      return `https://player.vimeo.com/video/${vimeoMatch[1]}`;
    return null;
  }

  onMount(async () => {
    try {
      fetch("http://127.0.0.1:5000/api/analytics/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "property_view", property_id: id }),
      }).catch(console.error);

      const [propResponse, allPropsResponse] = await Promise.all([
        fetch(`http://127.0.0.1:5000/api/properties/${id}`),
        fetch(`http://127.0.0.1:5000/api/properties`),
      ]);

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

      user.subscribe(async (u) => {
        if (u) {
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

<div class="min-h-screen bg-background pb-20">
  {#if loading}
    <div class="container py-8 space-y-8">
      <Skeleton class="h-[500px] w-full rounded-2xl" />
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-4">
          <Skeleton class="h-12 w-3/4" />
          <Skeleton class="h-6 w-1/2" />
          <Skeleton class="h-40 w-full" />
        </div>
        <Skeleton class="h-[400px] w-full rounded-xl" />
      </div>
    </div>
  {:else if error}
    <div
      class="flex flex-col items-center justify-center min-h-[60vh] text-center px-4"
    >
      <h2 class="text-2xl font-bold text-destructive mb-2">
        Error Loading Property
      </h2>
      <p class="text-muted-foreground mb-6">{error}</p>
      <Button variant="outline" href="/properties">Back to Properties</Button>
    </div>
  {:else if property}
    <!-- Hero / Gallery Section -->
    <ImageGallery
      images={property.images && property.images.length > 0
        ? property.images
        : [property.imageUrl]}
      title={property.title}
    />

    <div class="container -mt-20 relative z-30">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Info -->
        <div class="lg:col-span-2 space-y-8">
          <Card
            class="border-none shadow-2xl overflow-hidden backdrop-blur-sm bg-card/95"
          >
            <CardContent class="p-8">
              <div
                class="flex flex-col md:flex-row justify-between items-start gap-4 mb-6"
              >
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <Badge
                      variant="secondary"
                      class="bg-primary/10 text-primary hover:bg-primary/20 border-none"
                    >
                      {property.type}
                    </Badge>
                    <Badge variant="outline" class="text-muted-foreground">
                      ID: {property.id}
                    </Badge>
                  </div>
                  <h1
                    class="text-3xl md:text-4xl font-bold tracking-tight mb-2"
                  >
                    {property.title}
                  </h1>
                  <div class="flex items-center text-muted-foreground text-lg">
                    <MapPin class="w-5 h-5 mr-2 text-primary" />
                    {property.location}
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-3xl font-bold text-primary mb-2">
                    ₹ {property.price}
                  </div>
                  <div class="flex gap-2 justify-end">
                    <Button
                      variant="ghost"
                      size="icon"
                      onclick={toggleFavorite}
                      class="hover:bg-red-50 hover:text-red-500"
                    >
                      <Heart
                        class="w-5 h-5 {isFavorite
                          ? 'fill-red-500 text-red-500'
                          : ''}"
                      />
                    </Button>
                    <Button variant="ghost" size="icon" onclick={handleShare}>
                      <Share2 class="w-5 h-5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onclick={handlePrint}
                      class="no-print"
                    >
                      <Printer class="w-5 h-5" />
                    </Button>
                  </div>
                </div>
              </div>

              <Separator class="my-6" />

              <div class="grid grid-cols-3 gap-4 md:gap-8">
                <div
                  class="flex flex-col items-center p-4 rounded-2xl bg-muted/30 hover:bg-muted/50 transition-colors"
                >
                  <Bed class="w-8 h-8 mb-2 text-primary" />
                  <span class="text-2xl font-bold">{property.bedrooms}</span>
                  <span class="text-sm text-muted-foreground">Bedrooms</span>
                </div>
                <div
                  class="flex flex-col items-center p-4 rounded-2xl bg-muted/30 hover:bg-muted/50 transition-colors"
                >
                  <Bath class="w-8 h-8 mb-2 text-primary" />
                  <span class="text-2xl font-bold">{property.bathrooms}</span>
                  <span class="text-sm text-muted-foreground">Bathrooms</span>
                </div>
                <div
                  class="flex flex-col items-center p-4 rounded-2xl bg-muted/30 hover:bg-muted/50 transition-colors"
                >
                  <Maximize class="w-8 h-8 mb-2 text-primary" />
                  <span class="text-2xl font-bold"
                    >{property.sqft || property.area || "N/A"}</span
                  >
                  <span class="text-sm text-muted-foreground">Sq Ft</span>
                </div>
              </div>

              <div class="mt-8">
                <h3 class="text-xl font-bold mb-4">About this home</h3>
                <p class="text-muted-foreground leading-relaxed text-lg">
                  {property.description ||
                    "Experience luxury living in this stunning property. Featuring modern amenities, spacious interiors, and a prime location, this home offers the perfect blend of comfort and style."}
                </p>
              </div>
            </CardContent>
          </Card>

          <!-- Map Section -->
          <Card class="overflow-hidden border-none shadow-lg">
            <CardHeader>
              <CardTitle>Location</CardTitle>
            </CardHeader>
            <CardContent class="p-0 h-[400px]">
              <Map
                lat={property.lat || 19.076}
                lng={property.lng || 72.8777}
                zoom={15}
              />
            </CardContent>
          </Card>

          <!-- Video Section -->
          {#if property.videoUrl}
            <Card class="overflow-hidden border-none shadow-lg">
              <CardHeader>
                <CardTitle>Video Tour</CardTitle>
              </CardHeader>
              <CardContent class="p-0 aspect-video bg-black">
                {#if property.videoType === "file" || !getEmbedUrl(property.videoUrl)}
                  <video src={property.videoUrl} controls class="w-full h-full">
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
              </CardContent>
            </Card>
          {/if}
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <div class="sticky top-24 space-y-6">
            <ContactAgentForm
              propertyId={property.id}
              propertyTitle={property.title}
            />

            <MortgageCalculator
              price={parseInt(property.price.replace(/[^0-9]/g, ""))}
            />
          </div>
        </div>
      </div>

      {#if similarProperties.length > 0}
        <div class="mt-16 mb-8">
          <h2 class="text-2xl font-bold mb-6">You Might Also Like</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {#each similarProperties as prop}
              <a href="/properties/{prop.id}" class="block group">
                <Card
                  class="overflow-hidden border-none shadow-md hover:shadow-xl transition-all duration-300"
                >
                  <div class="aspect-[4/3] overflow-hidden relative">
                    <img
                      src={prop.imageUrl ||
                        prop.images?.[0] ||
                        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
                      alt={prop.title}
                      class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div
                      class="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors"
                    ></div>
                    <Badge
                      class="absolute top-2 left-2 bg-white/90 text-black hover:bg-white"
                    >
                      {prop.type}
                    </Badge>
                  </div>
                  <CardContent class="p-4">
                    <h4
                      class="font-bold text-lg line-clamp-1 group-hover:text-primary transition-colors"
                    >
                      {prop.title}
                    </h4>
                    <p class="text-muted-foreground text-sm mb-2 line-clamp-1">
                      {prop.location}
                    </p>
                    <p class="font-bold text-primary text-lg">₹ {prop.price}</p>
                  </CardContent>
                </Card>
              </a>
            {/each}
          </div>
        </div>
      {/if}
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
        class="flex flex-col h-24 gap-2 hover:bg-green-50 hover:border-green-200"
        onclick={() => shareSocial("whatsapp")}
      >
        <span class="text-2xl">📱</span>
        WhatsApp
      </Button>
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2 hover:bg-blue-50 hover:border-blue-200"
        onclick={() => shareSocial("facebook")}
      >
        <Facebook class="w-6 h-6 text-blue-600" />
        Facebook
      </Button>
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2 hover:bg-sky-50 hover:border-sky-200"
        onclick={() => shareSocial("twitter")}
      >
        <Twitter class="w-6 h-6 text-sky-500" />
        Twitter
      </Button>
      <Button
        variant="outline"
        class="flex flex-col h-24 gap-2 hover:bg-gray-50"
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
    :global(.embla__button) {
      display: none !important;
    }
  }
</style>
