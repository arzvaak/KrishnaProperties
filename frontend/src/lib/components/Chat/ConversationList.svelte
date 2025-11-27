<script>
    import { createEventDispatcher } from "svelte";
    import { user } from "$lib/stores/auth";
    import { Search } from "lucide-svelte";

    export let conversations = [];
    export let selectedConversationId = null;

    const dispatch = createEventDispatcher();
    let searchQuery = "";

    $: filteredConversations = conversations.filter((conv) => {
        // In a real app, we'd fetch user details to search by name
        // For now, we search by ID or last message
        const searchLower = searchQuery.toLowerCase();
        return (
            conv.id.toLowerCase().includes(searchLower) ||
            (conv.lastMessage?.text || "").toLowerCase().includes(searchLower)
        );
    });

    function selectConversation(id) {
        dispatch("select", { id });
    }

    function formatTime(timestamp) {
        if (!timestamp) return "";
        const date = timestamp.toDate();
        const now = new Date();
        const diff = now - date;

        if (diff < 24 * 60 * 60 * 1000) {
            return date.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            });
        }
        return date.toLocaleDateString();
    }
</script>

<div class="flex flex-col h-full bg-white border-r border-gray-200 w-80">
    <div class="p-4 border-b border-gray-200">
        <h2 class="text-xl font-bold mb-4">Messages</h2>
        <div class="relative">
            <Search
                class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                size={18}
            />
            <input
                type="text"
                placeholder="Search conversations..."
                bind:value={searchQuery}
                class="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm"
            />
        </div>
    </div>

    <div class="flex-1 overflow-y-auto">
        {#each filteredConversations as conv}
            <button
                class="w-full p-4 flex items-start gap-3 hover:bg-gray-50 transition-colors text-left {selectedConversationId ===
                conv.id
                    ? 'bg-blue-50 border-r-4 border-primary'
                    : ''}"
                on:click={() => selectConversation(conv.id)}
            >
                <div
                    class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0 font-semibold text-gray-600"
                >
                    {conv.id[0].toUpperCase()}
                </div>

                <div class="flex-1 min-w-0">
                    <div class="flex justify-between items-baseline mb-1">
                        <h3 class="font-semibold truncate text-gray-900">
                            User {conv.id.slice(0, 6)}...
                        </h3>
                        <span
                            class="text-xs text-gray-500 whitespace-nowrap ml-2"
                        >
                            {formatTime(conv.updatedAt)}
                        </span>
                    </div>

                    <p
                        class="text-sm text-gray-600 truncate {conv
                            .unreadCount?.[$user?.uid] > 0
                            ? 'font-bold text-black'
                            : ''}"
                    >
                        {#if conv.lastMessage?.senderId === $user?.uid}
                            <span class="text-gray-400">You: </span>
                        {/if}
                        {conv.lastMessage?.text || "Attachment"}
                    </p>
                </div>

                {#if conv.unreadCount?.[$user?.uid] > 0}
                    <div
                        class="w-5 h-5 rounded-full bg-primary text-white text-xs flex items-center justify-center flex-shrink-0 mt-1"
                    >
                        {conv.unreadCount[$user.uid]}
                    </div>
                {/if}
            </button>
        {/each}

        {#if filteredConversations.length === 0}
            <div class="p-8 text-center text-gray-500">
                <p>No conversations found</p>
            </div>
        {/if}
    </div>
</div>
