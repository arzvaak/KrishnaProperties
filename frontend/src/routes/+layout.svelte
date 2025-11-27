<script>
  import "../app.css";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import { Toaster } from "$lib/components/ui/sonner";
  import { page } from "$app/stores";

  let { children } = $props();
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
</div>
