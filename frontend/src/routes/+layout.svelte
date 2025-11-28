<script>
  import { onMount } from "svelte";
  import { user } from "$lib/stores/auth";
  import { settings } from "$lib/stores/settings";
  import { API_BASE_URL } from "$lib/config";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import { Toaster } from "$lib/components/ui/sonner";
  import { ModeWatcher } from "mode-watcher";
  import ComparisonFloatingBar from "$lib/components/comparison/ComparisonFloatingBar.svelte";
  import { page } from "$app/stores";
  import "../app.css";

  let { children } = $props();

  onMount(async () => {
    await fetchPublicSettings();
  });

  async function fetchPublicSettings() {
    try {
      const res = await fetch(`${API_BASE_URL}/api/settings/public`);
      if (res.ok) {
        const data = await res.json();
        settings.update((s) => ({
          ...s,
          general: { ...s.general, ...data.general },
          contact: { ...s.contact, ...data.contact },
          social: { ...s.social, ...data.social },
          seo: { ...s.seo, ...data.seo },
        }));
      }
    } catch (e) {
      console.error("Failed to fetch settings", e);
    }
  }
</script>

<svelte:head>
  <title>{$settings.seo.defaultTitle}</title>
  <meta name="description" content={$settings.seo.defaultDescription} />
  <meta name="keywords" content={$settings.seo.defaultKeywords} />
</svelte:head>

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
