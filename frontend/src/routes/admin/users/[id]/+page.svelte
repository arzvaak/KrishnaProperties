<script lang="ts">
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import { Separator } from "$lib/components/ui/separator";
    import { Label } from "$lib/components/ui/label";
    import { toast } from "svelte-sonner";
    import { goto } from "$app/navigation";
    import {
        ArrowLeft,
        Phone,
        Calendar,
        ShieldAlert,
        ShieldCheck,
        Activity,
    } from "lucide-svelte";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let user: any = null;
    let loading = true;
    let processing = false;
    let stats = { inquiries: 0, favorites: 0 };
    let activity: any[] = [];

    const userId = $page.params.id;

    async function loadData() {
        try {
            const [userRes, statsRes, activityRes] = await Promise.all([
                fetchWithAuth(`${API_BASE_URL}/api/admin/users/${userId}`),
                fetchWithAuth(
                    `${API_BASE_URL}/api/admin/users/${userId}/stats`,
                ),
                fetchWithAuth(
                    `${API_BASE_URL}/api/admin/users/${userId}/activity`,
                ),
            ]);

            if (userRes.ok) user = await userRes.json();
            if (statsRes.ok) stats = await statsRes.json();
            if (activityRes.ok) activity = await activityRes.json();
        } catch (e) {
            console.error("Failed to load user data", e);
            toast.error("Failed to load user data");
        } finally {
            loading = false;
        }
    }

    onMount(loadData);

    async function updateStatus(status: string) {
        if (
            !confirm(
                `Are you sure you want to ${status === "suspended" ? "suspend" : "activate"} this user?`,
            )
        )
            return;

        processing = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/users/${userId}/status`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ status }),
                },
            );

            if (res.ok) {
                toast.success(
                    `User ${status === "suspended" ? "suspended" : "activated"} successfully`,
                );
                await loadData();
            } else {
                toast.error("Failed to update status");
            }
        } catch (e) {
            toast.error("Error updating status");
        } finally {
            processing = false;
        }
    }

    async function updateRole(role: string) {
        if (
            !confirm(
                `Are you sure you want to change this user's role to ${role}?`,
            )
        ) {
            await loadData(); // Reset selection
            return;
        }

        processing = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/users/${userId}/role`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ role }),
                },
            );

            if (res.ok) {
                toast.success("Role updated successfully");
            } else {
                toast.error("Failed to update role");
                await loadData(); // Revert on failure
            }
        } catch (e) {
            toast.error("Error updating role");
            await loadData();
        } finally {
            processing = false;
        }
    }
</script>

<div class="space-y-6">
    <Button variant="ghost" class="gap-2" onclick={() => goto("/admin/users")}>
        <ArrowLeft class="w-4 h-4" /> Back to Users
    </Button>

    {#if loading}
        <div class="text-center py-12">Loading user details...</div>
    {:else if user}
        <div class="grid gap-6 md:grid-cols-3">
            <!-- Profile Card -->
            <Card class="md:col-span-1">
                <CardHeader>
                    <CardTitle>Profile</CardTitle>
                </CardHeader>
                <CardContent
                    class="flex flex-col items-center text-center space-y-4"
                >
                    {#if user.photoURL}
                        <img
                            src={user.photoURL}
                            alt={user.displayName}
                            class="w-24 h-24 rounded-full object-cover border-4 border-muted"
                        />
                    {:else}
                        <div
                            class="w-24 h-24 rounded-full bg-muted flex items-center justify-center text-2xl font-bold"
                        >
                            {(user.displayName ||
                                user.email ||
                                "?")[0].toUpperCase()}
                        </div>
                    {/if}

                    <div>
                        <h2 class="text-xl font-bold">
                            {user.displayName || "Unknown Name"}
                        </h2>
                        <p class="text-sm text-muted-foreground">
                            {user.email}
                        </p>
                    </div>

                    <Badge
                        variant={user.status === "suspended"
                            ? "destructive"
                            : "default"}
                        class="text-sm px-3 py-1"
                    >
                        {user.status || "Active"}
                    </Badge>

                    <div class="w-full space-y-2 text-left pt-4">
                        <div class="flex items-center gap-2 text-sm">
                            <Phone class="w-4 h-4 text-muted-foreground" />
                            <span>{user.phoneNumber || "No phone"}</span>
                        </div>
                        <div class="flex items-center gap-2 text-sm">
                            <Calendar class="w-4 h-4 text-muted-foreground" />
                            <span
                                >Joined: {user.createdAt
                                    ? new Date(
                                          user.createdAt,
                                      ).toLocaleDateString()
                                    : "Unknown"}</span
                            >
                        </div>
                    </div>

                    <Separator />

                    <div class="w-full space-y-3">
                        <Label
                            class="text-xs font-semibold uppercase text-muted-foreground"
                            >Role Management</Label
                        >
                        <div class="flex gap-2">
                            <select
                                class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                                bind:value={user.role}
                                onchange={() => updateRole(user.role)}
                                disabled={processing}
                            >
                                <option value="user">User</option>
                                <option value="admin">Admin</option>
                                <option value="superadmin">Superadmin</option>
                            </select>
                        </div>
                    </div>

                    <Separator />

                    <div class="w-full pt-2">
                        {#if user.status === "suspended"}
                            <Button
                                variant="outline"
                                class="w-full gap-2 text-green-600 hover:text-green-700"
                                onclick={() => updateStatus("active")}
                                disabled={processing}
                            >
                                <ShieldCheck class="w-4 h-4" /> Activate User
                            </Button>
                        {:else}
                            <Button
                                variant="outline"
                                class="w-full gap-2 text-destructive hover:text-destructive"
                                onclick={() => updateStatus("suspended")}
                                disabled={processing}
                            >
                                <ShieldAlert class="w-4 h-4" /> Suspend User
                            </Button>
                        {/if}
                    </div>
                </CardContent>
            </Card>

            <div class="md:col-span-2 space-y-6">
                <!-- Stats Grid -->
                <div class="grid grid-cols-2 gap-4">
                    <Card>
                        <CardHeader class="pb-2">
                            <CardTitle
                                class="text-sm font-medium text-muted-foreground"
                                >Total Inquiries</CardTitle
                            >
                        </CardHeader>
                        <CardContent>
                            <div class="text-2xl font-bold">
                                {stats.inquiries}
                            </div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader class="pb-2">
                            <CardTitle
                                class="text-sm font-medium text-muted-foreground"
                                >Saved Favorites</CardTitle
                            >
                        </CardHeader>
                        <CardContent>
                            <div class="text-2xl font-bold">
                                {stats.favorites}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                <!-- Activity Log -->
                <Card>
                    <CardHeader>
                        <CardTitle class="flex items-center gap-2">
                            <Activity class="w-5 h-5" /> Recent Activity
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {#if activity.length === 0}
                            <p class="text-muted-foreground text-center py-4">
                                No recent activity.
                            </p>
                        {:else}
                            <div class="space-y-4">
                                {#each activity as event}
                                    <div
                                        class="flex items-start gap-4 pb-4 border-b last:border-0 last:pb-0"
                                    >
                                        <div
                                            class="text-xs text-muted-foreground w-24 shrink-0 pt-1"
                                        >
                                            {event.timestamp
                                                ? new Date(
                                                      event.timestamp,
                                                  ).toLocaleString()
                                                : "Unknown"}
                                        </div>
                                        <div>
                                            <p
                                                class="font-medium text-sm capitalize"
                                            >
                                                {event.type.replace("_", " ")}
                                            </p>
                                            {#if event.property_id}
                                                <p
                                                    class="text-xs text-muted-foreground"
                                                >
                                                    Property ID: {event.property_id}
                                                </p>
                                            {/if}
                                            {#if event.metadata}
                                                <p
                                                    class="text-xs text-muted-foreground"
                                                >
                                                    {JSON.stringify(
                                                        event.metadata,
                                                    )}
                                                </p>
                                            {/if}
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </CardContent>
                </Card>
            </div>
        </div>
    {:else}
        <div class="text-center py-12 text-red-500">User not found</div>
    {/if}
</div>
