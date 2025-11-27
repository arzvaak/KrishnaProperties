<script>
    import { onMount } from "svelte";
    import { db } from "$lib/firebase";
    import { collection, query, orderBy, onSnapshot } from "firebase/firestore";
    import ChatWindow from "$lib/components/Chat/ChatWindow.svelte";
    import ConversationList from "$lib/components/Chat/ConversationList.svelte";
    import { user } from "$lib/stores/auth";

    let conversations = [];
    let selectedConversationId = null;
    let unsubscribe;

    onMount(() => {
        // Admin sees all conversations
        // In a real app with many users, we might paginate or search
        // For now, we listen to all conversations
        const q = query(
            collection(db, "conversations"),
            orderBy("updatedAt", "desc"),
        );

        unsubscribe = onSnapshot(q, (snapshot) => {
            conversations = snapshot.docs.map((doc) => ({
                id: doc.id,
                ...doc.data(),
            }));
        });

        return () => {
            if (unsubscribe) unsubscribe();
        };
    });

    function handleSelect(event) {
        selectedConversationId = event.detail.id;
    }
</script>

<div class="flex h-[calc(100vh-4rem)] bg-gray-100">
    <!-- Sidebar List -->
    <ConversationList
        {conversations}
        {selectedConversationId}
        on:select={handleSelect}
    />

    <!-- Chat Area -->
    <div class="flex-1 p-6 flex flex-col">
        {#if selectedConversationId}
            <ChatWindow
                conversationId={selectedConversationId}
                recipientId={selectedConversationId}
                recipientName={`User ${selectedConversationId.slice(0, 6)}`}
            />
        {:else}
            <div
                class="flex-1 flex items-center justify-center text-gray-400 flex-col gap-4"
            >
                <div
                    class="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="40"
                        height="40"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        ><path
                            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                        /></svg
                    >
                </div>
                <p class="text-lg font-medium">
                    Select a conversation to start chatting
                </p>
            </div>
        {/if}
    </div>
</div>
