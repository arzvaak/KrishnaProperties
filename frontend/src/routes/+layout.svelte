<script>
  import "../app.css";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import { Toaster } from "$lib/components/ui/sonner";
</script>

<div class="min-h-screen flex flex-col font-sans antialiased">
  <Navbar />
  <main class="flex-1">
    <slot />
  </main>
  <Footer />
  <Toaster />
</div>
