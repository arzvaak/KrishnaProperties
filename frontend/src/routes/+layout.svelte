<script>
  import "../app.css";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import { Toaster } from "$lib/components/ui/sonner";
  import ComparisonFloatingBar from "$lib/components/comparison/ComparisonFloatingBar.svelte";
  import { page } from "$app/stores";

  import { onMount } from "svelte";

  let { children } = $props();

  onMount(() => {
    const loader = document.getElementById("app-loader");
    if (loader) {
      loader.style.opacity = "0";
      setTimeout(() => loader.remove(), 500);
    }
  });
</script>

<div
  class="min-h-screen bg-background flex flex-col font-sans text-foreground antialiased selection:bg-primary/20 selection:text-primary relative"
>
  <!-- Subtle Background Texture Removed -->

  <Navbar />
  <main class="flex-1 flex flex-col">
    {@render children()}
  </main>
  <Footer />
  <Toaster />
  <ComparisonFloatingBar />
</div>
