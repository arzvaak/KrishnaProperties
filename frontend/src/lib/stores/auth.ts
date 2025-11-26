import { writable, type Writable, derived } from 'svelte/store';
import { auth } from '$lib/firebase';
import { onAuthStateChanged, type User } from 'firebase/auth';

export const user: Writable<User | null> = writable(null);
export const loading = writable(true);
export const isAdmin = writable(false);

onAuthStateChanged(auth, async (currentUser) => {
    user.set(currentUser);
    if (currentUser) {
        const tokenResult = await currentUser.getIdTokenResult();
        isAdmin.set(!!tokenResult.claims.admin);
    } else {
        isAdmin.set(false);
    }
    loading.set(false);
});
