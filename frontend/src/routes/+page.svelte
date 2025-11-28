<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Card, CardContent } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { reveal } from "$lib/actions/reveal";
  import FeaturedCollection from "$lib/components/FeaturedCollection.svelte";
  import StatsSection from "$lib/components/home/StatsSection.svelte";
  import TestimonialsSection from "$lib/components/home/TestimonialsSection.svelte";
  import WhyChooseUsSection from "$lib/components/home/WhyChooseUsSection.svelte";
  import NewsletterSection from "$lib/components/home/NewsletterSection.svelte";
  import {
    CheckCircle2,
    Users,
    TrendingUp,
    Search,
    Sparkles,
  } from "lucide-svelte";
  import { user } from "$lib/stores/auth";

  let properties: any[] = [];
  let featuredProperties: any[] = [];
  let loading = true;

  import { API_BASE_URL } from "$lib/config";

  onMount(async () => {
    try {
      // Track Page View
      fetch(`${API_BASE_URL}/api/analytics/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "page_view",
          page: "/",
          user_id: $user ? $user.uid : null,
        }),
      }).catch(console.error);

      const response = await fetch(`${API_BASE_URL}/api/properties`);
      if (response.ok) {
        const data = await response.json();
        properties = data.properties || [];
        featuredProperties = properties.slice(0, 3); // Top 3 for featured
      }
    } catch (error) {
      console.error("Failed to fetch properties:", error);
    } finally {
      loading = false;
    }
  });
</script>

<div class="flex flex-col min-h-screen bg-background">
  <!-- Hero Section -->
  <section
    class="relative h-[80vh] min-h-[600px] flex items-center justify-center overflow-hidden"
  >
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0 z-0">
      <img
        src="/images/hero-bg-v2.png"
        alt="Luxury Villa"
        class="w-full h-full object-cover"
      />
      <div
        class="absolute inset-0 bg-gradient-to-b from-black/70 via-black/40 to-background/90"
      ></div>
    </div>

    <!-- Hero Content -->
    <div class="container relative z-10 px-4 text-center" use:reveal>
      <Badge
        variant="outline"
        class="mb-6 text-white border-white/30 backdrop-blur-md px-4 py-1 text-sm uppercase tracking-widest"
      >
        Exclusive Real Estate
      </Badge>
      <h1
        class="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 tracking-tight leading-tight"
      >
        Discover Your <br />
        <span
          class="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 to-yellow-500"
        >
          Dream Sanctuary
        </span>
      </h1>
      <p
        class="text-lg md:text-xl text-gray-200 mb-10 max-w-2xl mx-auto font-light leading-relaxed"
      >
        Curated properties for those who seek the extraordinary.
      </p>

      <!-- Search & Dream Home Finder -->
      <div class="max-w-4xl mx-auto flex flex-col gap-4">
        <!-- Search Bar -->
        <div
          class="bg-white/10 backdrop-blur-xl border border-white/20 p-2 rounded-full flex flex-col md:flex-row gap-2 shadow-2xl"
        >
          <div class="flex-1 relative">
            <Search
              class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5"
            />
            <Input
              type="text"
              placeholder="Search by location, property type..."
              class="pl-12 h-12 bg-transparent border-none text-white placeholder:text-gray-300 focus-visible:ring-0 text-lg rounded-full"
            />
          </div>
          <Button
            size="lg"
            class="h-12 px-8 rounded-full bg-primary text-primary-foreground hover:bg-primary/90 text-lg font-medium shadow-lg"
          >
            Search
          </Button>
        </div>

        <!-- Dream Home CTA -->
        <div
          class="flex items-center justify-center gap-2 text-white/90 text-sm"
        >
          <span>Looking for something specific?</span>
          <a
            href="/requests"
            class="flex items-center gap-1 text-amber-300 hover:text-amber-200 font-medium transition-colors group"
          >
            <Sparkles class="w-4 h-4" />
            Try our Dream Home Finder
            <TrendingUp
              class="w-3 h-3 group-hover:translate-x-1 transition-transform"
            />
          </a>
        </div>
      </div>

      <!-- Stats Component -->
      <StatsSection />
    </div>
  </section>

  <!-- Featured Collections -->
  <FeaturedCollection properties={featuredProperties} {loading} />

  <!-- Why Choose Us Component -->
  <WhyChooseUsSection />

  <!-- Dream Home Finder (Dark Section) -->
  <section class="relative py-32 overflow-hidden">
    <div class="absolute inset-0">
      <img
        src="/images/interior-bg.png"
        alt="Interior"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-primary/90 mix-blend-multiply"></div>
    </div>

    <div class="container relative z-10 px-4">
      <div class="grid md:grid-cols-2 gap-16 items-center">
        <div use:reveal>
          <div
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-amber-300 text-sm font-medium mb-6"
          >
            <Sparkles class="w-4 h-4" />
            <span>Concierge Service</span>
          </div>
          <h2
            class="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight"
          >
            Can't find exactly <br /> what you need?
          </h2>
          <p class="text-xl text-gray-300 mb-8 leading-relaxed">
            Our "Dream Home Finder" service is designed for discerning clients.
            Tell us your requirements, and our dedicated agents will scour the
            market—including off-market listings—to find your perfect match.
          </p>
          <Button
            size="lg"
            class="bg-amber-500 hover:bg-amber-600 text-black font-semibold px-8 h-14 rounded-full"
            href="/requests"
          >
            Start Your Search
          </Button>
        </div>

        <div class="grid gap-6" use:reveal={{ delay: 200 }}>
          <Card class="bg-white/5 backdrop-blur-md border-white/10 text-white">
            <CardContent class="p-6 flex items-start gap-4">
              <div class="p-3 rounded-full bg-amber-500/20 text-amber-400">
                <CheckCircle2 class="w-6 h-6" />
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">Priority Access</h3>
                <p class="text-gray-400">
                  Be the first to know about new listings before they hit the
                  public market.
                </p>
              </div>
            </CardContent>
          </Card>
          <Card class="bg-white/5 backdrop-blur-md border-white/10 text-white">
            <CardContent class="p-6 flex items-start gap-4">
              <div class="p-3 rounded-full bg-amber-500/20 text-amber-400">
                <Users class="w-6 h-6" />
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">Dedicated Agent</h3>
                <p class="text-gray-400">
                  A personal real estate expert assigned specifically to your
                  search.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials Component -->
  <TestimonialsSection />

  <!-- Newsletter Component -->
  <NewsletterSection />

  <!-- Final CTA -->
  <section class="py-32 bg-background text-center">
    <div class="container px-4" use:reveal>
      <h2 class="text-4xl md:text-6xl font-bold mb-8">
        Ready to elevate your lifestyle?
      </h2>
      <p class="text-xl text-muted-foreground mb-12 max-w-2xl mx-auto">
        Let us guide you home to the luxury you deserve.
      </p>
      <Button
        size="lg"
        class="h-16 px-10 text-xl rounded-full shadow-xl"
        href="/contact"
      >
        Contact Us Today
      </Button>
    </div>
  </section>
</div>
