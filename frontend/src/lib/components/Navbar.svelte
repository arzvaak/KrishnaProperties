<script lang="ts">
  import { user, isAdmin } from "$lib/stores/auth";
  import { Button } from "$lib/components/ui/button";
  import { auth } from "$lib/firebase";
  import { signOut } from "firebase/auth";
  import { goto } from "$app/navigation";

  import { MessageCircle } from "lucide-svelte";
  import { db } from "$lib/firebase";
  import { doc, onSnapshot } from "firebase/firestore";
  import { onDestroy } from "svelte";

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

  $: if ($user) {
    if (unsubscribe) unsubscribe();

    if ($isAdmin) {
      // Admin: Listen to all conversations with unread messages for admin
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

        // Initial load shouldn't trigger toast unless we want it to
        // But simpler to just track increase
        if (newMessages) {
          toast.info("You have new messages");
        }

        unreadCount = totalUnread;
        previousUnreadCount = totalUnread;
      });
    } else {
      // User: Listen to their own conversation
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
        {#if $isAdmin}
          <a
            href="/admin"
            class="text-sm font-bold text-primary hover:underline"
            >Admin Panel</a
          >
          <a
            href="/admin/messages"
            class="relative text-gray-600 hover:text-primary transition-colors"
          >
            <MessageCircle size={20} />
            {#if unreadCount > 0}
              <span
                class="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center"
              >
                {unreadCount}
              </span>
            {/if}
          </a>
        {/if}
        {#if !$isAdmin}
          <a
            href="/messages"
            class="relative text-gray-600 hover:text-primary transition-colors"
          >
            <MessageCircle size={20} />
            {#if unreadCount > 0}
              <span
                class="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center"
              >
                {unreadCount}
              </span>
            {/if}
          </a>
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
      {:else}
        <div class="flex items-center gap-2">
          <Button variant="ghost" size="sm" href="/login">Login</Button>
          <Button size="sm" href="/register">Sign Up</Button>
        </div>
      {/if}
    </div>
  </div>
</nav>
