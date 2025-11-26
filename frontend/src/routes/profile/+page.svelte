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
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
        CardDescription,
        CardFooter,
    } from "$lib/components/ui/card";
    import { toast } from "svelte-sonner";
    import { Loader2, User, Phone, Mail } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import { deleteUser } from "firebase/auth";

    let loading = false;
    let isEditing = false;
    let profile = {
        displayName: "",
        email: "",
        phoneNumber: "",
        bio: "",
        photoURL: "",
        emailNotifications: false, // Default to false
    };

    onMount(() => {
        user.subscribe((u) => {
            if (u) {
                profile = {
                    displayName: u.displayName || "",
                    email: u.email || "",
                    phoneNumber: u.phoneNumber || "",
                    bio: (u as any).bio || "",
                    photoURL: u.photoURL || "",
                    emailNotifications: false, // Default to false
                };
                fetchProfile(u.uid);
            }
        });
    });

    async function fetchProfile(uid: string) {
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/users/${uid}`);
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
            const res = await fetch(
                `http://127.0.0.1:5000/api/users/${$user.uid}`,
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
            isEditing = false;
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
            // 1. Call backend to delete user data
            const res = await fetch(
                `http://127.0.0.1:5000/api/users/${$user.uid}`,
                {
                    method: "DELETE",
                },
            );

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || "Failed to delete account data");
            }

            // 2. Delete user from Firebase Auth
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

    function handleCancel() {
        isEditing = false;
        if ($user) fetchProfile($user.uid);
    }
</script>

<div class="container py-10 max-w-2xl">
    <Card>
        <CardHeader>
            <div class="flex justify-between items-start">
                <div>
                    <CardTitle class="text-2xl">My Profile</CardTitle>
                    <CardDescription
                        >Manage your personal information</CardDescription
                    >
                </div>
                {#if !isEditing}
                    <Button variant="outline" onclick={() => (isEditing = true)}
                        >Edit Profile</Button
                    >
                {/if}
            </div>
        </CardHeader>
        <CardContent class="space-y-6">
            <!-- Avatar Section -->
            <div class="flex flex-col items-center space-y-4">
                <Avatar.Root class="h-24 w-24">
                    <Avatar.Image
                        src={profile.photoURL}
                        alt={profile.displayName}
                    />
                    <Avatar.Fallback class="text-2xl"
                        >{profile.displayName?.charAt(0) ||
                            "U"}</Avatar.Fallback
                    >
                </Avatar.Root>
                {#if isEditing}
                    <div class="w-full max-w-sm">
                        <Label for="photoURL">Avatar URL</Label>
                        <div class="flex gap-2 mt-1">
                            <Input
                                id="photoURL"
                                bind:value={profile.photoURL}
                                placeholder="https://..."
                            />
                        </div>
                        <p class="text-xs text-muted-foreground mt-1">
                            Enter a URL for your profile picture.
                        </p>
                    </div>
                {/if}
            </div>

            <div class="grid gap-4">
                <div class="grid gap-2">
                    <Label for="name">Display Name</Label>
                    {#if isEditing}
                        <div class="relative">
                            <User
                                class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                            />
                            <Input
                                id="name"
                                bind:value={profile.displayName}
                                class="pl-9"
                            />
                        </div>
                    {:else}
                        <div
                            class="flex items-center p-2 border rounded-md bg-muted/50"
                        >
                            <User class="mr-2 h-4 w-4 text-muted-foreground" />
                            {profile.displayName || "Not set"}
                        </div>
                    {/if}
                </div>

                <div class="grid gap-2">
                    <Label for="email">Email</Label>
                    <div
                        class="flex items-center p-2 border rounded-md bg-muted/50 opacity-70 cursor-not-allowed"
                    >
                        <Mail class="mr-2 h-4 w-4 text-muted-foreground" />
                        {profile.email}
                    </div>
                    <p class="text-xs text-muted-foreground">
                        Email cannot be changed.
                    </p>
                </div>

                <div class="grid gap-2">
                    <Label for="phone">Phone Number</Label>
                    {#if isEditing}
                        <div class="relative">
                            <Phone
                                class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                            />
                            <Input
                                id="phone"
                                bind:value={profile.phoneNumber}
                                class="pl-9"
                                placeholder="+91 98765 43210"
                            />
                        </div>
                    {:else}
                        <div
                            class="flex items-center p-2 border rounded-md bg-muted/50"
                        >
                            <Phone class="mr-2 h-4 w-4 text-muted-foreground" />
                            {profile.phoneNumber || "Not set"}
                        </div>
                    {/if}
                </div>

                <div class="grid gap-2">
                    <Label for="bio">Bio</Label>
                    {#if isEditing}
                        <div class="relative">
                            <Textarea
                                id="bio"
                                bind:value={profile.bio}
                                placeholder="Tell us about yourself..."
                                class="min-h-[100px]"
                            />
                        </div>
                    {:else}
                        <div
                            class="p-3 border rounded-md bg-muted/50 min-h-[60px] whitespace-pre-wrap"
                        >
                            {profile.bio || "No bio added yet."}
                        </div>
                    {/if}
                </div>
            </div>

            <div class="pt-6 border-t">
                <h3 class="text-lg font-medium mb-4">
                    Notification Preferences
                </h3>
                <div class="flex items-center justify-between space-x-2">
                    <Label
                        for="email-notifications"
                        class="flex flex-col space-y-1"
                    >
                        <span>Email Notifications</span>
                        <span class="font-normal text-xs text-muted-foreground">
                            Receive updates about your inquiries and
                            appointments.
                        </span>
                    </Label>
                    <Switch
                        id="email-notifications"
                        bind:checked={profile.emailNotifications}
                        disabled={!isEditing}
                    />
                </div>
            </div>

            <div class="pt-6 border-t">
                <h3 class="text-lg font-medium mb-4 text-destructive">
                    Danger Zone
                </h3>
                <div
                    class="flex items-center justify-between p-4 border border-destructive/50 rounded-lg bg-destructive/5"
                >
                    <div class="space-y-1">
                        <p class="font-medium text-destructive">
                            Delete Account
                        </p>
                        <p class="text-sm text-muted-foreground">
                            Permanently delete your account and all data.
                        </p>
                    </div>
                    <AlertDialog.Root>
                        <AlertDialog.Trigger>
                            <Button variant="destructive">Delete Account</Button
                            >
                        </AlertDialog.Trigger>
                        <AlertDialog.Content>
                            <AlertDialog.Header>
                                <AlertDialog.Title
                                    >Are you absolutely sure?</AlertDialog.Title
                                >
                                <AlertDialog.Description>
                                    This action cannot be undone. This will
                                    permanently delete your account and remove
                                    your data from our servers.
                                </AlertDialog.Description>
                            </AlertDialog.Header>
                            <AlertDialog.Footer>
                                <AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
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
        </CardContent>
        {#if isEditing}
            <CardFooter class="flex justify-end gap-2">
                <Button
                    variant="ghost"
                    onclick={handleCancel}
                    disabled={loading}>Cancel</Button
                >
                <Button onclick={handleSave} disabled={loading}>
                    {#if loading}
                        <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                        Saving...
                    {:else}
                        Save Changes
                    {/if}
                </Button>
            </CardFooter>
        {/if}
    </Card>
</div>
