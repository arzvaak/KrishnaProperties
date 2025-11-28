<script lang="ts">
    import { onMount } from "svelte";
    import { user } from "$lib/stores/auth";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";
    import { Switch } from "$lib/components/ui/switch";
    import * as Avatar from "$lib/components/ui/avatar";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { toast } from "svelte-sonner";
    import {
        Loader2,
        User,
        Phone,
        Mail,
        Settings,
        Shield,
        Bell,
    } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import { deleteUser } from "firebase/auth";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let loading = false;
    let activeTab = "general";
    let profile = {
        displayName: "",
        email: "",
        phoneNumber: "",
        bio: "",
        photoURL: "",
        emailNotifications: false,
    };

    const tabs = [
        { id: "general", label: "General", icon: User },
        { id: "preferences", label: "Preferences", icon: Bell },
        { id: "settings", label: "Settings", icon: Settings },
    ];

    onMount(() => {
        user.subscribe((u) => {
            if (u) {
                profile = {
                    displayName: u.displayName || "",
                    email: u.email || "",
                    phoneNumber: u.phoneNumber || "",
                    bio: (u as any).bio || "",
                    photoURL: u.photoURL || "",
                    emailNotifications: false,
                };
                fetchProfile(u.uid);
            }
        });
    });

    async function fetchProfile(uid: string) {
        try {
            const res = await fetchWithAuth(`${API_BASE_URL}/api/users/${uid}`);
            if (res.ok) {
                const data = await res.json();
                profile = { ...profile, ...data };
            }
        } catch (e) {
            console.error("Failed to fetch profile", e);
        }
    }

    async function handleSave() {
        if (!$user) return;
        loading = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/users/${$user.uid}`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        displayName: profile.displayName,
                        phoneNumber: profile.phoneNumber,
                        bio: profile.bio,
                        photoURL: profile.photoURL,
                        emailNotifications: profile.emailNotifications,
                    }),
                },
            );

            if (!res.ok) throw new Error("Failed to update profile");

            toast.success("Profile updated successfully");
        } catch (e: any) {
            toast.error(e.message);
        } finally {
            loading = false;
        }
    }

    async function handleDeleteAccount() {
        if (!$user) return;
        loading = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/users/${$user.uid}`,
                {
                    method: "DELETE",
                },
            );

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || "Failed to delete account data");
            }

            await deleteUser($user);
            toast.success("Account deleted successfully");
            goto("/");
        } catch (e: any) {
            console.error("Delete error:", e);
            if (e.code === "auth/requires-recent-login") {
                toast.error("Please log in again to delete your account.");
            } else {
                toast.error(e.message || "Failed to delete account");
            }
        } finally {
            loading = false;
        }
    }
</script>

<div class="container py-10 pt-24 max-w-5xl">
    <div class="mb-8">
        <h1 class="text-3xl font-bold tracking-tight">Account Settings</h1>
        <p class="text-muted-foreground">
            Manage your profile and preferences.
        </p>
    </div>

    <div class="flex flex-col md:flex-row gap-8">
        <!-- Sidebar -->
        <aside class="w-full md:w-64 flex-shrink-0">
            <nav class="flex flex-col space-y-1">
                {#each tabs as tab}
                    <button
                        onclick={() => (activeTab = tab.id)}
                        class={`flex items-center gap-3 px-4 py-2.5 text-sm font-medium rounded-md transition-colors ${
                            activeTab === tab.id
                                ? "bg-primary text-primary-foreground"
                                : "text-muted-foreground hover:bg-muted hover:text-foreground"
                        }`}
                    >
                        <svelte:component this={tab.icon} size={18} />
                        {tab.label}
                    </button>
                {/each}
            </nav>
        </aside>

        <!-- Content -->
        <div class="flex-1 max-w-2xl">
            {#if !profile.email && loading}
                <div class="space-y-6">
                    <div
                        class="bg-card rounded-xl border shadow-sm p-6 space-y-6"
                    >
                        <div class="space-y-2">
                            <Skeleton class="h-6 w-40" />
                            <Skeleton class="h-4 w-60" />
                        </div>
                        <div class="flex items-center gap-6">
                            <Skeleton class="h-20 w-20 rounded-full" />
                            <div class="space-y-2 flex-1">
                                <Skeleton class="h-4 w-24" />
                            </div>
                        </div>
                        <p class="text-sm text-muted-foreground mb-6">
                            Update your photo and personal details.
                        </p>

                        <div class="space-y-6">
                            <!-- Avatar -->
                            <div class="flex items-center gap-6">
                                <Avatar.Root
                                    class="h-20 w-20 border-2 border-muted"
                                >
                                    <Avatar.Image
                                        src={profile.photoURL}
                                        alt={profile.displayName}
                                    />
                                    <Avatar.Fallback class="text-xl"
                                        >{profile.displayName?.charAt(0) ||
                                            "U"}</Avatar.Fallback
                                    >
                                </Avatar.Root>
                                <div class="flex-1 space-y-2">
                                    <Label for="photoURL">Avatar URL</Label>
                                    <Input
                                        id="photoURL"
                                        bind:value={profile.photoURL}
                                        placeholder="https://..."
                                    />
                                </div>
                            </div>

                            <div class="grid gap-4">
                                <div class="grid gap-2">
                                    <Label for="name">Display Name</Label>
                                    <Input
                                        id="name"
                                        bind:value={profile.displayName}
                                    />
                                </div>

                                <div class="grid gap-2">
                                    <Label for="email">Email</Label>
                                    <Input
                                        id="email"
                                        value={profile.email}
                                        disabled
                                        class="bg-muted/50"
                                    />
                                    <p
                                        class="text-[10px] text-muted-foreground"
                                    >
                                        Email cannot be changed.
                                    </p>
                                </div>

                                <div class="grid gap-2">
                                    <Label for="phone">Phone Number</Label>
                                    <Input
                                        id="phone"
                                        bind:value={profile.phoneNumber}
                                        placeholder="+91..."
                                    />
                                </div>

                                <div class="grid gap-2">
                                    <Label for="bio">Bio</Label>
                                    <Textarea
                                        id="bio"
                                        bind:value={profile.bio}
                                        placeholder="Tell us about yourself..."
                                        class="min-h-[100px]"
                                    />
                                </div>
                            </div>
                        </div>

                        <div class="mt-6 flex justify-end">
                            <Button onclick={handleSave} disabled={loading}>
                                {#if loading}
                                    <Loader2
                                        class="mr-2 h-4 w-4 animate-spin"
                                    />
                                    Saving...
                                {:else}
                                    Save Changes
                                {/if}
                            </Button>
                        </div>
                    </div>
                </div>
            {:else if activeTab === "preferences"}
                <div
                    class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500"
                >
                    <div class="bg-card rounded-xl border shadow-sm p-6">
                        <h2 class="text-lg font-semibold mb-1">
                            Notifications
                        </h2>
                        <p class="text-sm text-muted-foreground mb-6">
                            Manage how you receive updates.
                        </p>

                        <div class="flex items-center justify-between py-4">
                            <div class="space-y-0.5">
                                <Label class="text-base"
                                    >Email Notifications</Label
                                >
                                <p class="text-sm text-muted-foreground">
                                    Receive updates about your inquiries and
                                    appointments.
                                </p>
                            </div>
                            <Switch
                                bind:checked={profile.emailNotifications}
                                onCheckedChange={handleSave}
                            />
                        </div>
                    </div>
                </div>
            {:else if activeTab === "settings"}
                <div
                    class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500"
                >
                    <div
                        class="bg-card rounded-xl border border-destructive/20 shadow-sm p-6"
                    >
                        <h2 class="text-lg font-semibold mb-1 text-destructive">
                            Danger Zone
                        </h2>
                        <p class="text-sm text-muted-foreground mb-6">
                            Irreversible actions for your account.
                        </p>

                        <div
                            class="flex items-center justify-between p-4 border border-destructive/20 rounded-lg bg-destructive/5"
                        >
                            <div class="space-y-1">
                                <p class="font-medium text-destructive">
                                    Delete Account
                                </p>
                                <p class="text-sm text-muted-foreground">
                                    Permanently delete your account and all
                                    data.
                                </p>
                            </div>
                            <AlertDialog.Root>
                                <AlertDialog.Trigger>
                                    <Button variant="destructive" size="sm"
                                        >Delete Account</Button
                                    >
                                </AlertDialog.Trigger>
                                <AlertDialog.Content>
                                    <AlertDialog.Header>
                                        <AlertDialog.Title
                                            >Are you absolutely sure?</AlertDialog.Title
                                        >
                                        <AlertDialog.Description>
                                            This action cannot be undone. This
                                            will permanently delete your account
                                            and remove your data from our
                                            servers.
                                        </AlertDialog.Description>
                                    </AlertDialog.Header>
                                    <AlertDialog.Footer>
                                        <AlertDialog.Cancel
                                            >Cancel</AlertDialog.Cancel
                                        >
                                        <AlertDialog.Action
                                            class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                                            onclick={handleDeleteAccount}
                                        >
                                            Delete Account
                                        </AlertDialog.Action>
                                    </AlertDialog.Footer>
                                </AlertDialog.Content>
                            </AlertDialog.Root>
                        </div>
                    </div>
                </div>
            {:else if activeTab === "notifications"}
                <div
                    class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500"
                >
                    <div class="bg-card rounded-xl border shadow-sm p-6">
                        <h2 class="text-xl font-bold mb-4">
                            Notification Preferences
                        </h2>
                        <div class="space-y-6">
                            <div class="flex items-center justify-between">
                                <div class="space-y-0.5">
                                    <span class="text-sm font-medium"
                                        >Email Notifications</span
                                    >
                                    <p class="text-xs text-muted-foreground">
                                        Receive updates via email
                                    </p>
                                </div>
                                <Switch checked={true} />
                            </div>
                            <div class="flex items-center justify-between">
                                <div class="space-y-0.5">
                                    <span class="text-sm font-medium"
                                        >Push Notifications</span
                                    >
                                    <p class="text-xs text-muted-foreground">
                                        Receive updates in browser
                                    </p>
                                </div>
                                <Switch checked={true} />
                            </div>
                            <div class="flex items-center justify-between">
                                <div class="space-y-0.5">
                                    <span class="text-sm font-medium"
                                        >Marketing Emails</span
                                    >
                                    <p class="text-xs text-muted-foreground">
                                        Receive offers and news
                                    </p>
                                </div>
                                <Switch checked={false} />
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>
