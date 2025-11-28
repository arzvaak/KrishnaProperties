<script lang="ts">
    import { onMount } from "svelte";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";
    import { toast } from "svelte-sonner";
    import { auth } from "$lib/firebase";
    import { onAuthStateChanged } from "firebase/auth";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let user: any = null;
    let loading = true;
    let saving = false;

    let formData = {
        displayName: "",
        phoneNumber: "",
        bio: "",
        photoURL: "",
    };

    onMount(() => {
        const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
            if (currentUser) {
                user = currentUser;
                // Fetch additional profile data from Firestore if needed,
                // but for now we'll use what we have and assume a fetch from backend for full profile
                await loadProfile(currentUser.uid);
            } else {
                loading = false;
            }
        });
        return unsubscribe;
    });

    async function loadProfile(uid: string) {
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/users/${uid}/details`,
            );
            if (res.ok) {
                const data = await res.json();
                const profile = data.profile;
                formData = {
                    displayName: profile.displayName || "",
                    phoneNumber: profile.phoneNumber || "",
                    bio: profile.bio || "",
                    photoURL: profile.photoURL || "",
                };
            }
        } catch (e) {
            console.error("Error loading profile", e);
        } finally {
            loading = false;
        }
    }

    async function saveProfile() {
        if (!user) return;
        saving = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/users/${user.uid}`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(formData),
                },
            );

            if (res.ok) {
                toast.success("Profile updated successfully");
            } else {
                toast.error("Failed to update profile");
            }
        } catch (e) {
            toast.error("Error saving profile");
        } finally {
            saving = false;
        }
    }
</script>

<div class="space-y-6 max-w-2xl mx-auto">
    <div>
        <h1 class="text-3xl font-bold tracking-tight">My Profile</h1>
        <p class="text-muted-foreground">
            Manage your account settings and preferences.
        </p>
    </div>

    {#if loading}
        <div class="text-center py-12">Loading profile...</div>
    {:else if user}
        <Card>
            <CardHeader>
                <CardTitle>Personal Information</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
                <div class="space-y-2">
                    <Label for="email">Email</Label>
                    <Input
                        id="email"
                        value={user.email}
                        disabled
                        class="bg-muted"
                    />
                    <p class="text-xs text-muted-foreground">
                        Email cannot be changed.
                    </p>
                </div>

                <div class="space-y-2">
                    <Label for="displayName">Display Name</Label>
                    <Input
                        id="displayName"
                        bind:value={formData.displayName}
                        placeholder="Your Name"
                    />
                </div>

                <div class="space-y-2">
                    <Label for="photoURL">Avatar URL</Label>
                    <Input
                        id="photoURL"
                        bind:value={formData.photoURL}
                        placeholder="https://..."
                    />
                </div>

                <div class="space-y-2">
                    <Label for="phoneNumber">Phone Number</Label>
                    <Input
                        id="phoneNumber"
                        bind:value={formData.phoneNumber}
                        placeholder="+1 234 567 890"
                    />
                </div>

                <div class="space-y-2">
                    <Label for="bio">Bio</Label>
                    <Textarea
                        id="bio"
                        bind:value={formData.bio}
                        placeholder="Tell us about yourself"
                    />
                </div>

                <div class="pt-4 flex justify-end">
                    <Button onclick={saveProfile} disabled={saving}>
                        {saving ? "Saving..." : "Save Changes"}
                    </Button>
                </div>
            </CardContent>
        </Card>
    {:else}
        <div class="text-center py-12">Please log in to view your profile.</div>
    {/if}
</div>
