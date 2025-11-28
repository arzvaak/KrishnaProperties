<script lang="ts">
    import { notifications, unreadCount } from "$lib/stores/notifications";
    import { Bell, Check, Trash2, X } from "lucide-svelte";
    import { Button } from "$lib/components/ui/button";
    import { onMount } from "svelte";
    import { slide } from "svelte/transition";
    import * as Popover from "$lib/components/ui/popover";

    onMount(() => {
        notifications.fetch();
        // Poll every minute
        const interval = setInterval(() => notifications.fetch(), 60000);
        return () => clearInterval(interval);
    });

    function handleMarkRead(id: string, e: Event) {
        e.stopPropagation();
        notifications.markAsRead(id);
    }

    function handleDelete(id: string, e: Event) {
        e.stopPropagation();
        notifications.delete(id);
    }
</script>

<Popover.Root>
    <Popover.Trigger asChild let:builder>
        <Button
            builders={[builder]}
            variant="ghost"
            size="icon"
            class="relative text-white/80 hover:text-amber-400 hover:bg-white/10"
            aria-label="Notifications"
        >
            <Bell size={20} />
            {#if $unreadCount > 0}
                <span
                    class="absolute top-2 right-2 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-primary"
                ></span>
            {/if}
        </Button>
    </Popover.Trigger>
    <Popover.Content
        class="w-80 p-0 bg-card border-border shadow-xl"
        align="end"
    >
        <div
            class="p-4 border-b border-border flex justify-between items-center bg-muted/50"
        >
            <h3 class="font-semibold">Notifications</h3>
            {#if $unreadCount > 0}
                <Button
                    variant="ghost"
                    size="sm"
                    class="h-auto p-0 text-xs text-primary hover:text-primary/80"
                    onclick={() => notifications.markAllAsRead()}
                >
                    Mark all read
                </Button>
            {/if}
        </div>

        <div class="max-h-[400px] overflow-y-auto">
            {#if $notifications.length === 0}
                <div class="p-8 text-center text-muted-foreground">
                    <Bell class="w-8 h-8 mx-auto mb-2 opacity-20" />
                    <p class="text-sm">No notifications</p>
                </div>
            {:else}
                {#each $notifications as notification (notification.id)}
                    <div
                        class="p-4 border-b border-border/50 hover:bg-muted/50 transition-colors relative group {notification.read
                            ? 'opacity-60'
                            : 'bg-primary/5'}"
                    >
                        <div class="flex gap-3">
                            <div class="flex-1 min-w-0">
                                <h4 class="text-sm font-medium truncate pr-6">
                                    {notification.title}
                                </h4>
                                <p
                                    class="text-xs text-muted-foreground mt-1 line-clamp-2"
                                >
                                    {notification.message}
                                </p>
                                <span
                                    class="text-[10px] text-muted-foreground mt-2 block"
                                >
                                    {new Date(
                                        notification.createdAt,
                                    ).toLocaleDateString()}
                                </span>
                            </div>

                            <div
                                class="flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity absolute right-2 top-2"
                            >
                                {#if !notification.read}
                                    <button
                                        class="p-1 hover:bg-background rounded-full text-primary"
                                        onclick={(e) =>
                                            handleMarkRead(notification.id, e)}
                                        title="Mark as read"
                                    >
                                        <div
                                            class="w-1.5 h-1.5 bg-primary rounded-full"
                                        ></div>
                                    </button>
                                {/if}
                                <button
                                    class="p-1 hover:bg-destructive/10 hover:text-destructive rounded-full text-muted-foreground"
                                    onclick={(e) =>
                                        handleDelete(notification.id, e)}
                                    title="Delete"
                                >
                                    <X size={14} />
                                </button>
                            </div>
                        </div>
                    </div>
                {/each}
            {/if}
        </div>
    </Popover.Content>
</Popover.Root>
