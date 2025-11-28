<script lang="ts">
  import { user, isAdmin } from "$lib/stores/auth";
  import { Button } from "$lib/components/ui/button";
  import { auth } from "$lib/firebase";
  import { signOut } from "firebase/auth";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import { MessageCircle, Menu, X } from "lucide-svelte";
  import { db } from "$lib/firebase";
  import { doc, onSnapshot } from "firebase/firestore";
  import { onDestroy, onMount } from "svelte";

  import { slide } from "svelte/transition";
  import NotificationCenter from "$lib/components/NotificationCenter.svelte";

  import {
    collection,
    query,
    where,
    type QuerySnapshot,
    type DocumentData,
    type DocumentSnapshot,
  } from "firebase/firestore";
  import { toast } from "svelte-sonner";

  let unreadCount: number = 0;
  let unsubscribe: () => void;
  let previousUnreadCount: number = 0;
  let mobileMenuOpen = false;
  let scrolled = false;

  onMount(() => {
    const handleScroll = () => {
      scrolled = window.scrollY > 20;
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  });

  $: isHomepage = $page.url.pathname === "/";

  $: if ($user) {
    if (unsubscribe) unsubscribe();

    if ($isAdmin) {
      const q = query(
        collection(db, "conversations"),
        where("unreadCount.admin", ">", 0),
      );
      unsubscribe = onSnapshot(q, (snapshot: QuerySnapshot<DocumentData>) => {
        let totalUnread = 0;
        let newMessages = false;

        snapshot.docs.forEach((doc) => {
          const count = doc.data().unreadCount?.admin || 0;
          totalUnread += count;
        });

        if (totalUnread > previousUnreadCount && previousUnreadCount !== 0) {
          newMessages = true;
        }

        if (newMessages) {
          toast.info("You have new messages");
        }

        unreadCount = totalUnread;
        previousUnreadCount = totalUnread;
      });
    } else {
      unsubscribe = onSnapshot(
        doc(db, "conversations", $user.uid),
        (doc: DocumentSnapshot<DocumentData>) => {
          if (doc.exists()) {
            const data = doc.data();
            const count = data?.unreadCount?.[$user!.uid] || 0;

            if (count > previousUnreadCount && previousUnreadCount !== 0) {
              toast.info(
                `New message: ${data?.lastMessage?.text || "Attachment"}`,
              );
            }

            unreadCount = count;
            previousUnreadCount = count;
          } else {
            unreadCount = 0;
          }
        },
      );
    }
  } else if (unsubscribe) {
    unsubscribe();
    unreadCount = 0;
    previousUnreadCount = 0;
  }

  onDestroy(() => {
    if (unsubscribe) unsubscribe();
  });

  async function handleLogout() {
    await signOut(auth);
    goto("/");
  }

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }
</script>

<nav
  class={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
    scrolled
      ? "bg-primary/95 backdrop-blur-md shadow-lg py-2"
      : "bg-transparent py-6"
  } border-b ${scrolled ? "border-white/10" : "border-transparent"} text-primary-foreground`}
>
  <div class="container flex items-center justify-between">
    <a
      href="/"
      class="flex items-center gap-2 font-bold text-2xl tracking-tight"
    >
      <span class="text-amber-400">Krishna</span><span class="text-white"
        >Properties</span
      >
    </a>

    <!-- Desktop Menu -->
    <div class="hidden md:flex items-center gap-8">
      <a
        href="/properties"
        class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
        >Properties</a
      >
      <a
        href="/requests"
        class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
        >Dream Home</a
      >
      <a
        href="/about"
        class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
        >About</a
      >
      <a
        href="/contact"
        class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
        >Contact</a
      >
    </div>

    <div class="hidden md:flex items-center gap-4">
      {#if $user}
        {#if $isAdmin}
          <a
            href="/admin"
            class="text-sm font-bold text-amber-400 hover:text-amber-300 transition-colors"
            >Admin Panel</a
          >
          <a
            href="/admin/leads"
            class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
            >Leads</a
          >
        {/if}

        <a
          href={$isAdmin ? "/admin/messages" : "/messages"}
          class="relative text-white/80 hover:text-amber-400 transition-colors"
          aria-label="Messages"
        >
          <MessageCircle size={20} />
          {#if unreadCount > 0}
            <span
              class="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center shadow-sm"
            >
              {unreadCount}
            </span>
          {/if}
        </a>

        <NotificationCenter />

        <a
          href="/account/favorites"
          class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
          >Saved</a
        >
        <a
          href="/profile"
          class="text-sm font-medium text-white/80 hover:text-amber-400 transition-colors"
          >Profile</a
        >
        <Button
          variant="outline"
          size="sm"
          onclick={handleLogout}
          class="border-white/20 text-white hover:bg-white/10 hover:text-white bg-transparent"
        >
          Logout
        </Button>
      {:else}
        <div class="flex items-center gap-3">
          <a
            href="/login"
            class="text-sm font-medium text-white hover:text-amber-400 transition-colors"
            >Login</a
          >
          <Button
            size="sm"
            href="/register"
            class="bg-amber-500 hover:bg-amber-600 text-black font-semibold border-none"
            >Sign Up</Button
          >
        </div>
      {/if}
    </div>

    <!-- Mobile Menu Toggle -->
    <button
      class="md:hidden text-white"
      onclick={toggleMobileMenu}
      aria-label="Toggle mobile menu"
    >
      {#if mobileMenuOpen}
        <X size={24} />
      {:else}
        <Menu size={24} />
      {/if}
    </button>
  </div>

  <!-- Mobile Menu -->
  {#if mobileMenuOpen}
    <div
      transition:slide={{ duration: 300 }}
      class="md:hidden absolute top-full left-0 right-0 bg-primary border-b border-white/10 shadow-xl p-4 flex flex-col gap-4"
    >
      <a
        href="/properties"
        class="text-white/80 hover:text-amber-400"
        onclick={toggleMobileMenu}>Properties</a
      >
      <a
        href="/requests"
        class="text-white/80 hover:text-amber-400"
        onclick={toggleMobileMenu}>Dream Home</a
      >
      <a
        href="/about"
        class="text-white/80 hover:text-amber-400"
        onclick={toggleMobileMenu}>About</a
      >
      <a
        href="/contact"
        class="text-white/80 hover:text-amber-400"
        onclick={toggleMobileMenu}>Contact</a
      >
      <hr class="border-white/10" />
      {#if $user}
        <a
          href="/profile"
          class="text-white/80 hover:text-amber-400"
          onclick={toggleMobileMenu}>Profile</a
        >
        <button
          class="text-left text-white/80 hover:text-amber-400"
          onclick={() => {
            handleLogout();
            toggleMobileMenu();
          }}>Logout</button
        >
      {:else}
        <a
          href="/login"
          class="text-white/80 hover:text-amber-400"
          onclick={toggleMobileMenu}>Login</a
        >
        <a
          href="/register"
          class="text-amber-400 font-medium"
          onclick={toggleMobileMenu}>Sign Up</a
        >
      {/if}
    </div>
  {/if}
</nav>
