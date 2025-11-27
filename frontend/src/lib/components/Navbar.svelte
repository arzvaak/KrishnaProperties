<script lang="ts">
  import { user, isAdmin } from "$lib/stores/auth";
  import { Button } from "$lib/components/ui/button";
  import { auth } from "$lib/firebase";
  import { signOut } from "firebase/auth";
  import { goto } from "$app/navigation";

  async function handleLogout() {
    await signOut(auth);
    goto("/");
  }
</script>

<nav
  class="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50"
>
  <div class="container flex h-16 items-center justify-between">
    <a href="/" class="flex items-center gap-2 font-bold text-xl">
      <span class="text-primary">Krishna</span>Properties
    </a>

    <div class="hidden md:flex items-center gap-6">
      <a
        href="/properties"
        class="text-sm font-medium hover:text-primary transition-colors"
        >Properties</a
      >
      <a
        href="/requests"
        class="text-sm font-medium hover:text-primary transition-colors"
        >Dream Home</a
      >
      <a
        href="/about"
        class="text-sm font-medium hover:text-primary transition-colors"
        >About</a
      >
      <a
        href="/contact"
        class="text-sm font-medium hover:text-primary transition-colors"
        >Contact</a
      >
    </div>
    <div class="flex items-center gap-4">
      {#if $user}
        <div class="flex items-center gap-4">
          {#if $isAdmin}
            <a
              href="/admin"
              class="text-sm font-bold text-primary hover:underline"
              >Admin Panel</a
            >
          {/if}
          <a
            href="/account/favorites"
            class="text-sm font-medium hover:text-primary transition-colors"
            >Saved</a
          >
          <a
            href="/my-activity"
            class="text-sm font-medium hover:text-primary transition-colors"
            >My Activity</a
          >
          <a
            href="/profile"
            class="text-sm font-medium hover:text-primary transition-colors"
            >Profile</a
          >
          <Button variant="outline" size="sm" onclick={handleLogout}
            >Logout</Button
          >
        </div>
      {:else}
        <div class="flex items-center gap-2">
          <Button variant="ghost" size="sm" href="/login">Login</Button>
          <Button size="sm" href="/register">Sign Up</Button>
        </div>
      {/if}
    </div>
  </div>
</nav>
