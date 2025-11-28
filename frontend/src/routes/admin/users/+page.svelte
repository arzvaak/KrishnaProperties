<script lang="ts">
    import { onMount } from "svelte";
    import {
        Table,
        TableBody,
        TableCell,
        TableHead,
        TableHeader,
        TableRow,
    } from "$lib/components/ui/table";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Badge } from "$lib/components/ui/badge";
    import { Search, Eye } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let users: any[] = [];
    let filteredUsers: any[] = [];
    let search = "";
    let loading = true;

    onMount(async () => {
        try {
            const res = await fetchWithAuth(`${API_BASE_URL}/api/admin/users`);
            if (res.ok) {
                users = await res.json();
                filteredUsers = users;
            }
        } catch (e) {
            console.error("Failed to load users", e);
        } finally {
            loading = false;
        }
    });

    $: {
        if (search) {
            const lowerSearch = search.toLowerCase();
            filteredUsers = users.filter(
                (u) =>
                    (u.displayName || "").toLowerCase().includes(lowerSearch) ||
                    (u.email || "").toLowerCase().includes(lowerSearch),
            );
        } else {
            filteredUsers = users;
        }
    }

    function getStatusColor(status: string) {
        return status === "suspended" ? "destructive" : "default";
    }
</script>

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <h1 class="text-3xl font-bold tracking-tight">Users</h1>
        <div class="relative w-64">
            <Search
                class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground"
            />
            <Input
                placeholder="Search users..."
                class="pl-8"
                bind:value={search}
            />
        </div>
    </div>

    <div class="rounded-md border">
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Joined</TableHead>
                    <TableHead class="text-right">Actions</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {#if loading}
                    <TableRow>
                        <TableCell colspan={5} class="text-center py-8"
                            >Loading users...</TableCell
                        >
                    </TableRow>
                {:else if filteredUsers.length === 0}
                    <TableRow>
                        <TableCell colspan={5} class="text-center py-8"
                            >No users found.</TableCell
                        >
                    </TableRow>
                {:else}
                    {#each filteredUsers as user}
                        <TableRow>
                            <TableCell class="font-medium">
                                <div class="flex items-center gap-2">
                                    {#if user.photoURL}
                                        <img
                                            src={user.photoURL}
                                            alt={user.displayName}
                                            class="w-8 h-8 rounded-full object-cover"
                                        />
                                    {:else}
                                        <div
                                            class="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs font-bold"
                                        >
                                            {(user.displayName ||
                                                user.email ||
                                                "?")[0].toUpperCase()}
                                        </div>
                                    {/if}
                                    {user.displayName || "Unknown"}
                                </div>
                            </TableCell>
                            <TableCell>{user.email}</TableCell>
                            <TableCell>
                                <Badge
                                    variant={getStatusColor(
                                        user.status || "active",
                                    )}
                                >
                                    {user.status || "Active"}
                                </Badge>
                            </TableCell>
                            <TableCell>
                                {user.createdAt
                                    ? new Date(
                                          user.createdAt,
                                      ).toLocaleDateString()
                                    : "N/A"}
                            </TableCell>
                            <TableCell class="text-right">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    onclick={() =>
                                        goto(`/admin/users/${user.id}`)}
                                >
                                    <Eye class="w-4 h-4" />
                                </Button>
                            </TableCell>
                        </TableRow>
                    {/each}
                {/if}
            </TableBody>
        </Table>
    </div>
</div>
