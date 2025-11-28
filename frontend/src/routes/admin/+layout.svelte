<script lang="ts">
  import { user, loading, isAdmin } from "$lib/stores/auth";
  import { goto } from "$app/navigation";

  import { Button } from "$lib/components/ui/button";
  import {
    LayoutDashboard,
    PlusCircle,
    List,
    FileText,
    Settings,
    Users,
    Calendar,
    Loader2,
  } from "lucide-svelte";
  import { toast } from "svelte-sonner";

  let isAuthorized = false;
  let checking = true;

  $: if (!$loading) {
    if (!$user) {
      goto("/access-denied");
    } else {
      $user
        .getIdTokenResult()
        .then((token) => {
          if (token.claims.admin) {
            isAuthorized = true;
          } else {
            toast.error("Unauthorized access");
            goto("/access-denied");
          }
          checking = false;
        })
        .catch((e) => {
          console.error("Error checking admin claims:", e);
          goto("/access-denied");
          checking = false;
        });
    }
  }
</script>

{#if checking || !isAuthorized}
  <div class="h-screen w-full flex items-center justify-center">
    <Loader2 class="h-8 w-8 animate-spin text-primary" />
  </div>
{:else}
  <div class="flex min-h-screen pt-20">
    <!-- Sidebar -->
    <aside
      class="w-64 bg-muted/30 border-r hidden md:block fixed h-[calc(100vh-5rem)] overflow-y-auto"
    >
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
            href="/admin/leads"
          >
            <Users class="mr-2 h-4 w-4" /> Leads
          </Button>
          <Button
            variant="ghost"
            class="w-full justify-start"
            href="/admin/appointments"
          >
            <Calendar class="mr-2 h-4 w-4" /> Appointments
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
            href="/admin/blogs"
          >
            <FileText class="mr-2 h-4 w-4" /> Blogs
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
    <main class="flex-1 p-8 md:ml-64">
      <slot />
    </main>
  </div>
{/if}
