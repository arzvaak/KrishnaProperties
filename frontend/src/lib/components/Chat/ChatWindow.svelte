<script lang="ts">
    import { onMount, onDestroy, afterUpdate } from "svelte";
    import { db, storage } from "$lib/firebase";
    import {
        collection,
        query,
        orderBy,
        onSnapshot,
        addDoc,
        serverTimestamp,
        updateDoc,
        doc,
        increment,
        type QuerySnapshot,
        type DocumentData,
    } from "firebase/firestore";
    import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
    import {
        Send,
        Paperclip,
        X,
        File as FileIcon,
        Image as ImageIcon,
    } from "lucide-svelte";
    import { toast } from "svelte-sonner";
    import { user } from "$lib/stores/auth";

    export let conversationId: string;
    export let recipientId: string; // 'admin' or user uid
    export let recipientName: string = "Support";

    let messages: any[] = [];
    let newMessage: string = "";
    let fileInput: HTMLInputElement;
    let selectedFile: File | null = null;
    let isUploading: boolean = false;
    let unsubscribe: () => void;
    let chatContainer: HTMLDivElement;

    $: if (conversationId) {
        subscribeToMessages();
    }

    function subscribeToMessages() {
        if (unsubscribe) unsubscribe();

        const q = query(
            collection(db, "conversations", conversationId, "messages"),
            orderBy("timestamp", "asc"),
        );

        unsubscribe = onSnapshot(q, (snapshot: QuerySnapshot<DocumentData>) => {
            messages = snapshot.docs.map((doc) => ({
                id: doc.id,
                ...doc.data(),
            }));
            scrollToBottom();
            markAsRead();
        });
    }

    async function markAsRead() {
        if (!$user) return;
        try {
            // Call backend to mark as read to reset unread count
            await fetch("http://localhost:5000/api/chat/read", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ conversationId, userId: $user.uid }),
            });
        } catch (e) {
            console.error("Error marking read:", e);
        }
    }

    async function sendMessage() {
        if ((!newMessage.trim() && !selectedFile) || !$user) return;

        const messageText = newMessage.trim();
        const attachments = [];

        try {
            isUploading = true;

            if (selectedFile) {
                const storageRef = ref(
                    storage,
                    `chat/${conversationId}/${Date.now()}_${selectedFile.name}`,
                );
                await uploadBytes(storageRef, selectedFile);
                const url = await getDownloadURL(storageRef);
                attachments.push({
                    url,
                    type: selectedFile.type.startsWith("image/")
                        ? "image"
                        : "file",
                    name: selectedFile.name,
                });
            }

            // Send to backend to handle rate limiting and conversation creation logic if needed
            // But for speed, we can write directly to Firestore if we trust the client,
            // OR we stick to the plan and use the backend endpoint.
            // The plan said backend endpoint for rate limiting.

            const res = await fetch("http://localhost:5000/api/chat/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    senderId: $user.uid,
                    recipientId: recipientId,
                    text: messageText,
                    attachments,
                    conversationId: conversationId,
                }),
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || "Failed to send");
            }

            newMessage = "";
            selectedFile = null;
            isUploading = false;
        } catch (error) {
            console.error("Error sending message:", error);
            if (error instanceof Error) {
                toast.error(error.message);
            } else {
                toast.error("An unknown error occurred");
            }
            isUploading = false;
        }
    }

    function handleFileSelect(e: Event) {
        const target = e.target as HTMLInputElement;
        const file = target.files?.[0];
        if (file) {
            if (file.size > 5 * 1024 * 1024) {
                toast.error("File size must be less than 5MB");
                return;
            }
            selectedFile = file;
        }
    }

    function scrollToBottom() {
        if (chatContainer) {
            setTimeout(() => {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 100);
        }
    }

    onDestroy(() => {
        if (unsubscribe) unsubscribe();
    });
</script>

<div
    class="flex flex-col h-[600px] bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden"
>
    <!-- Header -->
    <div
        class="bg-primary px-4 py-3 flex items-center justify-between text-primary-foreground"
    >
        <div class="flex items-center gap-3">
            <div
                class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-lg font-bold"
            >
                {recipientName[0]}
            </div>
            <div>
                <h3 class="font-semibold">{recipientName}</h3>
                <span class="text-xs opacity-80">Online</span>
            </div>
        </div>
    </div>

    <!-- Messages -->
    <div
        class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50"
        bind:this={chatContainer}
    >
        {#each messages as msg}
            <div
                class="flex {msg.senderId === $user?.uid
                    ? 'justify-end'
                    : 'justify-start'}"
            >
                <div
                    class="max-w-[70%] {msg.senderId === $user?.uid
                        ? 'bg-primary text-primary-foreground rounded-br-none'
                        : 'bg-white border border-gray-200 rounded-bl-none'} rounded-2xl px-4 py-2 shadow-sm"
                >
                    {#if msg.attachments && msg.attachments.length > 0}
                        <div class="mb-2 space-y-2">
                            {#each msg.attachments as attachment}
                                {#if attachment.type === "image"}
                                    <img
                                        src={attachment.url}
                                        alt="attachment"
                                        class="rounded-lg max-h-48 object-cover cursor-pointer hover:opacity-90 transition-opacity"
                                    />
                                {:else}
                                    <a
                                        href={attachment.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        class="flex items-center gap-2 bg-black/10 p-2 rounded hover:bg-black/20 transition-colors"
                                    >
                                        <FileIcon size={16} />
                                        <span class="text-sm truncate"
                                            >{attachment.name}</span
                                        >
                                    </a>
                                {/if}
                            {/each}
                        </div>
                    {/if}

                    {#if msg.text}
                        <p class="text-sm whitespace-pre-wrap">{msg.text}</p>
                    {/if}

                    <div class="text-[10px] mt-1 opacity-70 text-right">
                        {msg.timestamp?.toDate().toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                        })}
                    </div>
                </div>
            </div>
        {/each}
    </div>

    <!-- Input -->
    <div class="p-4 bg-white border-t border-gray-200">
        {#if selectedFile}
            <div
                class="flex items-center gap-2 mb-2 p-2 bg-gray-100 rounded-lg w-fit"
            >
                <span class="text-sm truncate max-w-[200px]"
                    >{selectedFile.name}</span
                >
                <button
                    on:click={() => (selectedFile = null)}
                    class="text-gray-500 hover:text-red-500"
                >
                    <X size={16} />
                </button>
            </div>
        {/if}

        <div class="flex items-end gap-2">
            <input
                type="file"
                id="file-upload"
                class="hidden"
                bind:this={fileInput}
                on:change={handleFileSelect}
                accept="image/*,.pdf,.doc,.docx"
            />
            <button
                class="p-2 text-gray-500 hover:bg-gray-100 rounded-full transition-colors"
                on:click={() => fileInput.click()}
                disabled={isUploading}
            >
                <Paperclip size={20} />
            </button>

            <div class="flex-1 relative">
                <textarea
                    bind:value={newMessage}
                    placeholder="Type a message..."
                    class="w-full border border-gray-300 rounded-2xl px-4 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none max-h-32 min-h-[44px]"
                    rows="1"
                    on:keydown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            sendMessage();
                        }
                    }}
                ></textarea>
            </div>

            <button
                class="p-3 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
                on:click={sendMessage}
                disabled={(!newMessage.trim() && !selectedFile) || isUploading}
            >
                <Send size={18} />
            </button>
        </div>
    </div>
</div>
