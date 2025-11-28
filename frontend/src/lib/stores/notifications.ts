import { writable, derived } from "svelte/store";
import { API_BASE_URL } from "$lib/config";
import { fetchWithAuth } from "$lib/api";
import { toast } from "svelte-sonner";

interface Notification {
    id: string;
    title: string;
    message: string;
    type: "info" | "success" | "warning" | "error";
    read: boolean;
    createdAt: string;
    link?: string;
}

function createNotificationStore() {
    const { subscribe, set, update } = writable<Notification[]>([]);

    return {
        subscribe,
        set,
        fetch: async () => {
            try {
                const res = await fetchWithAuth(`${API_BASE_URL}/api/notifications/`);
                if (res.ok) {
                    const data = await res.json();
                    set(data);
                }
            } catch (error) {
                console.error("Failed to fetch notifications", error);
            }
        },
        markAsRead: async (id: string) => {
            // Optimistic update
            update(n => n.map(item => item.id === id ? { ...item, read: true } : item));

            try {
                await fetchWithAuth(`${API_BASE_URL}/api/notifications/${id}/read`, {
                    method: "PUT"
                });
            } catch (error) {
                console.error("Failed to mark as read", error);
            }
        },
        markAllAsRead: async () => {
            update(n => n.map(item => ({ ...item, read: true })));
            try {
                await fetchWithAuth(`${API_BASE_URL}/api/notifications/read-all`, {
                    method: "PUT"
                });
                toast.success("All marked as read");
            } catch (error) {
                console.error("Failed to mark all as read", error);
            }
        },
        delete: async (id: string) => {
            update(n => n.filter(item => item.id !== id));
            try {
                await fetchWithAuth(`${API_BASE_URL}/api/notifications/${id}`, {
                    method: "DELETE"
                });
                toast.success("Notification deleted");
            } catch (error) {
                console.error("Failed to delete notification", error);
                toast.error("Failed to delete");
            }
        }
    };
}

export const notifications = createNotificationStore();

export const unreadCount = derived(notifications, ($notifications) =>
    $notifications.filter(n => !n.read).length
);
