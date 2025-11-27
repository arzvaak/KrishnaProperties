<script lang="ts">
    import { user } from "$lib/stores/auth";
    import ChatWindow from "$lib/components/Chat/ChatWindow.svelte";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { Search, MessageSquare } from "lucide-svelte";
    import { Input } from "$lib/components/ui/input";

    let selectedConversation = "support";

    onMount(() => {
        if (!$user) {
            goto("/login?redirect=/messages");
        }
    });
</script>

<div class="h-[calc(100vh-4rem)] bg-gray-50 flex overflow-hidden pt-20">
    <!-- Sidebar -->
    <div class="w-80 bg-card border-r border-border flex flex-col">
        <div class="p-4 border-b border-gray-100">
            <h1 class="text-xl font-bold mb-4">Messages</h1>
            <div class="relative">
                <Search
                    class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                />
                <Input
                    placeholder="Search messages..."
                    class="pl-9 bg-gray-50"
                />
            </div>
        </div>

        <div class="flex-1 overflow-y-auto">
            <button
                class={`w-full p-4 flex items-start gap-3 hover:bg-gray-50 transition-colors text-left border-l-4 ${selectedConversation === "support" ? "bg-blue-50 border-primary" : "border-transparent"}`}
                onclick={() => (selectedConversation = "support")}
            >
                <div
                    class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold flex-shrink-0"
                >
                    S
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex justify-between items-baseline mb-1">
                        <h3 class="font-semibold text-sm truncate">
                            Customer Support
                        </h3>
                        <span class="text-[10px] text-gray-400">Now</span>
                    </div>
                    <p class="text-xs text-gray-500 truncate">
                        Welcome to Krishna Properties support!
                    </p>
                </div>
            </button>
        </div>
    </div>

    <!-- Chat Area -->
    <div class="flex-1 flex flex-col min-w-0 bg-card">
        {#if $user && selectedConversation === "support"}
            <ChatWindow
                conversationId={$user.uid}
                recipientId="admin"
                recipientName="Customer Support"
            />
        {:else}
            <div
                class="flex-1 flex flex-col items-center justify-center text-gray-400"
            >
                <div
                    class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4"
                >
                    <MessageSquare size={32} />
                </div>
                <p class="text-lg font-medium">Select a conversation</p>
            </div>
        {/if}
    </div>
</div>
