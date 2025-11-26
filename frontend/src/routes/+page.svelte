<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import PropertyCard from "$lib/components/PropertyCard.svelte";
  import emblaCarouselSvelte from "embla-carousel-svelte";
  import Autoplay from "embla-carousel-autoplay";
  import { reveal } from "$lib/actions/reveal";
  import {
    ArrowRight,
    CheckCircle2,
    Star,
    Users,
    Home,
    TrendingUp,
    ChevronLeft,
    ChevronRight,
  } from "lucide-svelte";
  import { Skeleton } from "$lib/components/ui/skeleton";

  let properties: any[] = [];
  let featuredProperties: any[] = [];
  let loading = true;
  let emblaApi: any;

  function onInit(event: CustomEvent) {
    emblaApi = event.detail;
  }

  function scrollPrev() {
    if (emblaApi) emblaApi.scrollPrev();
  }

  function scrollNext() {
    if (emblaApi) emblaApi.scrollNext();
  }

  onMount(async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/properties");
      if (response.ok) {
        properties = await response.json();
        // Take first 5 as featured for the carousel
        featuredProperties = properties.slice(0, 5);
      }
    } catch (error) {
      console.error("Failed to fetch properties:", error);
    } finally {
      loading = false;
    }
  });
</script>

<div class="flex flex-col min-h-screen">
  <!-- Hero Section with Carousel -->
  <section class="relative h-[700px] bg-black group">
    {#if loading}
      <Skeleton class="w-full h-full" />
    {:else if featuredProperties.length > 0}
      <div
        class="overflow-hidden h-full"
        use:emblaCarouselSvelte={{
          options: { loop: true },
          plugins: [Autoplay({ delay: 5000 })],
        }}
        onemblaInit={onInit}
      >
        <div class="flex h-full">
          {#each featuredProperties as property}
            <div class="flex-[0_0_100%] min-w-0 relative h-full">
              <div
                class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent z-10"
              ></div>
              <img
                src={property.imageUrl ||
                  property.images?.[0] ||
                  "https://images.unsplash.com/photo-1600596542815-27b88e35eabd?ixlib=rb-4.0.3&auto=format&fit=crop&w=2076&q=80"}
                alt={property.title}
                class="object-cover w-full h-full transform transition-transform duration-[10s] hover:scale-105"
              />
              <div
                class="absolute inset-0 z-20 flex items-center justify-center text-center text-white p-4"
              >
                <div class="max-w-4xl space-y-6">
                  <h1
                    class="text-5xl md:text-7xl font-bold tracking-tighter animate-in fade-in slide-in-from-bottom-4 duration-1000 drop-shadow-lg"
                  >
                    {property.title}
                  </h1>
                  <p
                    class="text-2xl md:text-3xl text-gray-200 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-200 font-light drop-shadow-md"
                  >
                    {property.location} •
                    <span class="font-semibold">₹ {property.price}</span>
                  </p>
                  <div
                    class="flex gap-4 justify-center animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-300 pt-4"
                  >
                    <Button
                      size="lg"
                      class="text-lg px-8 py-6 rounded-full shadow-lg hover:scale-105 transition-transform"
                      href="/properties/{property.id}">View Details</Button
                    >
                    <Button
                      size="lg"
                      variant="outline"
                      class="text-lg px-8 py-6 rounded-full bg-white/10 backdrop-blur-sm border-white/50 text-white hover:bg-white/20 hover:text-white hover:border-white transition-all hover:scale-105"
                      href="/contact">Contact Agent</Button
                    >
                  </div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      </div>

      <!-- Carousel Navigation -->
      <button
        class="absolute left-4 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-black/30 text-white backdrop-blur-md border border-white/10 hover:bg-black/50 transition-all opacity-0 group-hover:opacity-100"
        onclick={scrollPrev}
      >
        <ChevronLeft class="w-8 h-8" />
      </button>
      <button
        class="absolute right-4 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-black/30 text-white backdrop-blur-md border border-white/10 hover:bg-black/50 transition-all opacity-0 group-hover:opacity-100"
        onclick={scrollNext}
      >
        <ChevronRight class="w-8 h-8" />
      </button>
    {:else}
      <!-- Fallback if no properties -->
      <div
        class="relative h-full flex items-center justify-center text-center text-white"
      >
        <div class="absolute inset-0 bg-black/50 z-10"></div>
        <div
          class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1600596542815-27b88e35eabd?ixlib=rb-4.0.3&auto=format&fit=crop&w=2076&q=80')] bg-cover bg-center"
        ></div>
        <div class="relative z-20 container px-4">
          <h1 class="text-4xl md:text-6xl font-bold mb-6 tracking-tight">
            Find Your Dream Home
          </h1>
          <Button size="lg" class="text-lg px-8" href="/properties"
            >Browse Properties</Button
          >
        </div>
      </div>
    {/if}
  </section>

  <!-- Stats Section -->
  <section
    class="py-16 bg-primary text-primary-foreground relative overflow-hidden"
  >
    <div
      class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"
    ></div>
    <div class="container px-4 relative z-10" use:reveal>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
        <div
          class="p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-colors"
        >
          <div class="text-5xl font-bold mb-2">100+</div>
          <div class="text-primary-foreground/80 font-medium">
            Premium Listings
          </div>
        </div>
        <div
          class="p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-colors"
        >
          <div class="text-5xl font-bold mb-2">50+</div>
          <div class="text-primary-foreground/80 font-medium">
            Expert Agents
          </div>
        </div>
        <div
          class="p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-colors"
        >
          <div class="text-5xl font-bold mb-2">10k+</div>
          <div class="text-primary-foreground/80 font-medium">
            Happy Clients
          </div>
        </div>
        <div
          class="p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-colors"
        >
          <div class="text-5xl font-bold mb-2">24/7</div>
          <div class="text-primary-foreground/80 font-medium">Support</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Recent Listings Section -->
  <section class="py-24 bg-gradient-to-b from-background to-muted/30">
    <div class="container px-4">
      <div class="flex justify-between items-end mb-12" use:reveal>
        <div>
          <h2 class="text-4xl font-bold mb-4 tracking-tight">
            Recent Listings
          </h2>
          <p class="text-xl text-muted-foreground">
            Freshly added properties in prime locations
          </p>
        </div>
        <Button
          variant="ghost"
          href="/properties"
          class="hidden md:inline-flex gap-2 text-lg hover:bg-transparent hover:text-primary transition-colors"
        >
          View All <ArrowRight class="w-5 h-5" />
        </Button>
      </div>

      {#if loading}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          {#each Array(3) as _}
            <Skeleton class="h-[450px] w-full rounded-2xl" />
          {/each}
        </div>
      {:else}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          {#each properties.slice(0, 6) as property, i}
            <div use:reveal={{ threshold: 0.1 }}>
              <PropertyCard {property} />
            </div>
          {/each}
        </div>
      {/if}

      <div class="mt-12 text-center md:hidden">
        <Button variant="outline" size="lg" class="w-full" href="/properties"
          >View All Properties</Button
        >
      </div>
    </div>
  </section>

  <!-- Why Choose Us -->
  <section class="py-24 bg-muted/30 relative">
    <div class="container px-4">
      <div class="text-center max-w-3xl mx-auto mb-20" use:reveal>
        <h2 class="text-4xl font-bold mb-6 tracking-tight">
          Why Choose Krishna Real Estate?
        </h2>
        <p class="text-xl text-muted-foreground">
          We provide a seamless property buying experience with transparency,
          trust, and unparalleled service.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          class="bg-background p-10 rounded-2xl shadow-sm border hover:shadow-xl transition-all duration-300 hover:-translate-y-2 group"
          use:reveal={{ threshold: 0.2 }}
        >
          <div
            class="w-16 h-16 bg-primary/10 text-primary rounded-2xl flex items-center justify-center mx-auto mb-8 group-hover:bg-primary group-hover:text-white transition-colors duration-300"
          >
            <Home class="w-8 h-8" />
          </div>
          <h3 class="font-bold text-2xl mb-4">Wide Property Range</h3>
          <p class="text-muted-foreground text-lg leading-relaxed">
            From luxury villas to cozy apartments, we have properties for every
            budget and lifestyle.
          </p>
        </div>
        <div
          class="bg-background p-10 rounded-2xl shadow-sm border hover:shadow-xl transition-all duration-300 hover:-translate-y-2 group"
          use:reveal={{ threshold: 0.2 }}
        >
          <div
            class="w-16 h-16 bg-primary/10 text-primary rounded-2xl flex items-center justify-center mx-auto mb-8 group-hover:bg-primary group-hover:text-white transition-colors duration-300"
          >
            <Users class="w-8 h-8" />
          </div>
          <h3 class="font-bold text-2xl mb-4">Trusted Agents</h3>
          <p class="text-muted-foreground text-lg leading-relaxed">
            Our verified agents guide you through every step of the process with
            honesty and integrity.
          </p>
        </div>
        <div
          class="bg-background p-10 rounded-2xl shadow-sm border hover:shadow-xl transition-all duration-300 hover:-translate-y-2 group"
          use:reveal={{ threshold: 0.2 }}
        >
          <div
            class="w-16 h-16 bg-primary/10 text-primary rounded-2xl flex items-center justify-center mx-auto mb-8 group-hover:bg-primary group-hover:text-white transition-colors duration-300"
          >
            <TrendingUp class="w-8 h-8" />
          </div>
          <h3 class="font-bold text-2xl mb-4">Best Market Rates</h3>
          <p class="text-muted-foreground text-lg leading-relaxed">
            We ensure you get the best value for your investment with our deep
            market expertise.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials -->
  <section class="py-24 bg-background">
    <div class="container px-4">
      <h2
        class="text-4xl font-bold mb-16 text-center tracking-tight"
        use:reveal
      >
        What Our Clients Say
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {#each [1, 2, 3] as _, i}
          <div
            class="bg-muted/20 p-8 rounded-2xl border hover:border-primary/50 transition-colors"
            use:reveal={{ threshold: 0.1 }}
          >
            <div class="flex gap-1 text-yellow-500 mb-6">
              {#each Array(5) as _}<Star class="w-5 h-5 fill-current" />{/each}
            </div>
            <p
              class="text-muted-foreground mb-8 text-lg italic leading-relaxed"
            >
              "Found my dream home within weeks! The team was incredibly helpful
              and transparent throughout the process. Highly recommended!"
            </p>
            <div class="flex items-center gap-4">
              <div
                class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden ring-2 ring-primary/20"
              >
                <img
                  src={`https://api.dicebear.com/7.x/avataaars/svg?seed=Client${i}`}
                  alt="User"
                  class="w-full h-full object-cover"
                />
              </div>
              <div>
                <p class="font-bold text-base">Happy Client</p>
                <p class="text-sm text-muted-foreground">Homeowner</p>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section
    class="py-24 bg-primary text-primary-foreground text-center relative overflow-hidden"
  >
    <div
      class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"
    ></div>
    <div class="container px-4 relative z-10" use:reveal>
      <h2 class="text-4xl md:text-5xl font-bold mb-8 tracking-tight">
        Ready to Find Your New Home?
      </h2>
      <p
        class="text-2xl mb-10 text-primary-foreground/90 max-w-2xl mx-auto font-light"
      >
        Join thousands of satisfied customers who found their perfect property
        with us.
      </p>
      <Button
        size="lg"
        variant="secondary"
        class="text-xl px-10 py-8 rounded-full shadow-2xl hover:scale-105 transition-transform"
        href="/contact"
      >
        Get Started Today
      </Button>
    </div>
  </section>
</div>
