<script lang="ts">
  import { user, loading, isAdmin } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { LayoutDashboard, PlusCircle, List, Settings } from "lucide-svelte";
  import { toast } from "svelte-sonner";

  onMount(() => {
    const unsubscribe = user.subscribe(async (u) => {
      if (!loading) {
        if (!u) {
          goto("/login");
        } else {
          // Double check claims if user exists
          const token = await u.getIdTokenResult();
          if (!token.claims.admin) {
            toast.error("Unauthorized access");
            goto("/");
          }
        }
      }
    });
    return unsubscribe;
  });
</script>

<div class="flex min-h-screen">
  <!-- Sidebar -->
  <aside class="w-64 bg-muted/30 border-r hidden md:block">
    <div class="p-6">
      <h2 class="font-bold text-lg mb-6">Admin Panel</h2>
      <nav class="space-y-2">
        <Button variant="ghost" class="w-full justify-start" href="/admin">
          <LayoutDashboard class="mr-2 h-4 w-4" /> Dashboard
        </Button>
        <Button
          variant="ghost"
          class="w-full justify-start"
          href="/admin/properties"
        >
          <List class="mr-2 h-4 w-4" /> Properties
        </Button>
        <Button
          variant="ghost"
          class="w-full justify-start"
          href="/admin/properties/add"
        >
          <PlusCircle class="mr-2 h-4 w-4" /> Add Property
        </Button>
        <Button
          variant="ghost"
          class="w-full justify-start"
          href="/admin/settings"
        >
          <Settings class="mr-2 h-4 w-4" /> Settings
        </Button>
      </nav>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 p-8">
    <slot />
  </main>
</div>
