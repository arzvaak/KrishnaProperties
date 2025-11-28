import { auth } from "$lib/firebase";
import { API_BASE_URL } from "$lib/config";

type FetchOptions = RequestInit & {
    headers?: Record<string, string>;
};

export async function fetchWithAuth(endpoint: string, options: FetchOptions = {}) {
    const user = auth.currentUser;
    const headers: Record<string, string> = { ...options.headers } as Record<string, string>;

    if (user) {
        try {
            const token = await user.getIdToken();
            headers["Authorization"] = `Bearer ${token}`;
        } catch (error) {
            console.error("Error getting ID token:", error);
        }
    }

    // Ensure Content-Type is set for JSON requests if not already present
    if (!headers["Content-Type"] && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    // Construct full URL if endpoint is relative
    const url = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;

    const response = await fetch(url, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Handle unauthorized access (e.g., token expired or invalid)
        console.warn("Unauthorized access. User might need to log in again.");
        // You might want to trigger a logout or redirect here
    }

    return response;
}
