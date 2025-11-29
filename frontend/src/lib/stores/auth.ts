import { writable, type Writable, derived } from 'svelte/store';
import { auth } from '$lib/firebase';
import { onAuthStateChanged, type User } from 'firebase/auth';

export const user: Writable<User | null> = writable(null);
export const loading = writable(true);
export const isAdmin = writable(false);

onAuthStateChanged(auth, async (currentUser) => {
    user.set(currentUser);
    if (currentUser) {
        // Force token refresh to get the latest claims (e.g. admin role)
        const tokenResult = await currentUser.getIdTokenResult(true);
        isAdmin.set(!!tokenResult.claims.admin);
    } else {
        isAdmin.set(false);
    }
    loading.set(false);
});
