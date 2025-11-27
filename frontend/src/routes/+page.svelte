<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
  } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Separator } from "$lib/components/ui/separator";
  import { reveal } from "$lib/actions/reveal";
  import FeaturedCollection from "$lib/components/FeaturedCollection.svelte";
  import {
    CheckCircle2,
    Users,
    Home,
    TrendingUp,
    Search,
    Sparkles,
    Quote,
  } from "lucide-svelte";

  let properties: any[] = [];
  let featuredProperties: any[] = [];
  let loading = true;

  onMount(async () => {
    try {
      // Track site view
      fetch("http://127.0.0.1:5000/api/analytics/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "site_view" }),
      }).catch(console.error);

      const response = await fetch("http://127.0.0.1:5000/api/properties");
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
    class="relative h-screen min-h-[800px] flex items-center justify-center overflow-hidden"
  >
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0 z-0">
      <img
        src="/images/hero-bg.png"
        alt="Luxury Villa"
        class="w-full h-full object-cover"
      />
      <div
        class="absolute inset-0 bg-gradient-to-b from-black/70 via-black/40 to-background"
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
        class="text-5xl md:text-7xl lg:text-8xl font-bold text-white mb-6 tracking-tight leading-tight"
      >
        Discover Your <br />
        <span
          class="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 to-yellow-500"
        >
          Dream Sanctuary
        </span>
      </h1>
      <p
        class="text-xl md:text-2xl text-gray-200 mb-12 max-w-2xl mx-auto font-light leading-relaxed"
      >
        Curated properties for those who seek the extraordinary.
      </p>

      <!-- Search Bar -->
      <div
        class="max-w-4xl mx-auto bg-white/10 backdrop-blur-xl border border-white/20 p-2 rounded-full flex flex-col md:flex-row gap-2 shadow-2xl"
      >
        <div class="flex-1 relative">
          <Search
            class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5"
          />
          <Input
            type="text"
            placeholder="Search by location, property type..."
            class="pl-12 h-14 bg-transparent border-none text-white placeholder:text-gray-300 focus-visible:ring-0 text-lg rounded-full"
          />
        </div>
        <Button
          size="lg"
          class="h-14 px-8 rounded-full bg-primary text-primary-foreground hover:bg-primary/90 text-lg font-medium shadow-lg"
        >
          Search Properties
        </Button>
      </div>

      <!-- Stats -->
      <div
        class="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto text-white/90"
      >
        <div class="text-center">
          <div class="text-3xl font-bold mb-1">150+</div>
          <div class="text-sm uppercase tracking-wider opacity-70">
            Premium Listings
          </div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold mb-1">2k+</div>
          <div class="text-sm uppercase tracking-wider opacity-70">
            Happy Clients
          </div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold mb-1">50+</div>
          <div class="text-sm uppercase tracking-wider opacity-70">Cities</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold mb-1">24/7</div>
          <div class="text-sm uppercase tracking-wider opacity-70">Support</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Collections -->
  <FeaturedCollection properties={featuredProperties} {loading} />

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

  <!-- Why Choose Us -->
  <section class="py-32 bg-muted/30">
    <div class="container px-4">
      <div class="text-center max-w-3xl mx-auto mb-20" use:reveal>
        <h2 class="text-4xl font-bold mb-6">Why Choose Krishna Properties</h2>
        <p class="text-xl text-muted-foreground">
          Excellence in every detail of your real estate journey.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
        <div class="text-center group" use:reveal={{ threshold: 0.1 }}>
          <div
            class="w-20 h-20 mx-auto bg-background rounded-full flex items-center justify-center shadow-lg mb-8 group-hover:scale-110 transition-transform duration-300"
          >
            <Home class="w-8 h-8 text-primary" />
          </div>
          <h3 class="text-2xl font-bold mb-4">Premium Portfolio</h3>
          <p class="text-muted-foreground leading-relaxed">
            Access to the most exclusive and high-end properties in the market.
          </p>
        </div>
        <div
          class="text-center group"
          use:reveal={{ threshold: 0.1, delay: 100 }}
        >
          <div
            class="w-20 h-20 mx-auto bg-background rounded-full flex items-center justify-center shadow-lg mb-8 group-hover:scale-110 transition-transform duration-300"
          >
            <TrendingUp class="w-8 h-8 text-primary" />
          </div>
          <h3 class="text-2xl font-bold mb-4">Market Insight</h3>
          <p class="text-muted-foreground leading-relaxed">
            Deep data-driven analysis to ensure you make the best investment
            decisions.
          </p>
        </div>
        <div
          class="text-center group"
          use:reveal={{ threshold: 0.1, delay: 200 }}
        >
          <div
            class="w-20 h-20 mx-auto bg-background rounded-full flex items-center justify-center shadow-lg mb-8 group-hover:scale-110 transition-transform duration-300"
          >
            <Users class="w-8 h-8 text-primary" />
          </div>
          <h3 class="text-2xl font-bold mb-4">Personalized Care</h3>
          <p class="text-muted-foreground leading-relaxed">
            We treat every client's search as if it were our own.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials -->
  <section class="py-32 container px-4">
    <h2 class="text-4xl font-bold text-center mb-20">Client Stories</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each [1, 2, 3] as i}
        <Card class="bg-muted/30 border-none">
          <CardContent class="p-8">
            <Quote class="w-10 h-10 text-primary/20 mb-6" />
            <p class="text-lg text-muted-foreground mb-8 italic">
              "The level of service and attention to detail was outstanding.
              They truly understood what we were looking for."
            </p>
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden">
                <img
                  src={`https://api.dicebear.com/7.x/avataaars/svg?seed=Client${i}`}
                  alt="Client"
                />
              </div>
              <div>
                <div class="font-bold">Sarah Johnson</div>
                <div class="text-sm text-muted-foreground">
                  Luxury Villa Buyer
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      {/each}
    </div>
  </section>

  <!-- CTA -->
  <section class="py-32 bg-primary text-primary-foreground text-center">
    <div class="container px-4" use:reveal>
      <h2 class="text-4xl md:text-6xl font-bold mb-8">
        Ready to elevate your lifestyle?
      </h2>
      <p class="text-xl text-primary-foreground/80 mb-12 max-w-2xl mx-auto">
        Let us guide you home to the luxury you deserve.
      </p>
      <Button
        size="lg"
        variant="secondary"
        class="h-16 px-10 text-xl rounded-full"
        href="/contact"
      >
        Contact Us Today
      </Button>
    </div>
  </section>
</div>
