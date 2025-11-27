<script>
    import { user } from "$lib/stores/auth";
    import ChatWindow from "$lib/components/Chat/ChatWindow.svelte";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    onMount(() => {
        if (!$user) {
            goto("/login?redirect=/messages");
        }
    });
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <h1 class="text-3xl font-bold mb-6">Messages</h1>

    {#if $user}
        <div class="grid gap-6">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                <h2 class="font-semibold text-blue-800 mb-1">
                    Contact Support
                </h2>
                <p class="text-sm text-blue-600">
                    Have a question about a property? Chat directly with our
                    support team here.
                </p>
            </div>

            <!-- User always chats with 'admin' -->
            <!-- Conversation ID is the user's UID for simplicity in this 1:1 model -->
            <ChatWindow
                conversationId={$user.uid}
                recipientId="admin"
                recipientName="Customer Support"
            />
        </div>
    {/if}
</div>
