import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { user } from './auth';
import { API_BASE_URL } from '$lib/config';
import { fetchWithAuth } from '$lib/api';
import { toast } from 'svelte-sonner';

const STORAGE_KEY = 'property_comparison_list';

function createComparisonStore() {
    const { subscribe, set, update } = writable<string[]>([]);

    return {
        subscribe,
        init: async () => {
            if (!browser) return;

            const currentUser = get(user);

            if (currentUser) {
                // Fetch from Firebase
                try {
                    const res = await fetchWithAuth(`${API_BASE_URL}/api/users/${currentUser.uid}/comparison-list`);
                    if (res.ok) {
                        const ids = await res.json();
                        set(ids);
                    }
                } catch (e) {
                    console.error("Failed to fetch comparison list", e);
                }
            } else {
                // Load from localStorage
                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored) {
                    try {
                        set(JSON.parse(stored));
                    } catch (e) {
                        console.error("Failed to parse comparison list", e);
                    }
                }
            }
        },
        addProperty: async (id: string) => {
            let currentIds = get(comparison);
            if (currentIds.includes(id)) {
                toast.info("Property already in comparison");
                return;
            }
            if (currentIds.length >= 3) {
                toast.warning("You can compare up to 3 properties. Please remove one first.");
                return;
            }

            update(ids => {
                const newIds = [...ids, id];
                save(newIds);
                return newIds;
            });
            toast.success("Added to comparison");
        },
        removeProperty: async (id: string) => {
            update(ids => {
                const newIds = ids.filter(i => i !== id);
                save(newIds);
                return newIds;
            });
            toast.info("Removed from comparison");
        },
        toggleProperty: async (id: string) => {
            const currentIds = get(comparison);
            if (currentIds.includes(id)) {
                comparison.removeProperty(id);
            } else {
                comparison.addProperty(id);
            }
        },
        clear: async () => {
            set([]);
            save([]);
            toast.info("Comparison list cleared");
        }
    };
}

async function save(ids: string[]) {
    if (!browser) return;

    const currentUser = get(user);

    if (currentUser) {
        // Sync to Firebase
        try {
            await fetchWithAuth(`${API_BASE_URL}/api/users/${currentUser.uid}/comparison-list`, {
                method: 'PUT',
                body: JSON.stringify({ propertyIds: ids })
            });
        } catch (e) {
            console.error("Failed to sync comparison list", e);
        }
    } else {
        // Save to localStorage
        localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
    }
}

export const comparison = createComparisonStore();

// Re-init when user changes (login/logout)
user.subscribe(() => {
    if (browser) {
        comparison.init();
    }
});
