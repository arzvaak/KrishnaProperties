<script lang="ts">
    import { onMount } from "svelte";
    import * as Tabs from "$lib/components/ui/tabs";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import {
        Table,
        TableBody,
        TableCell,
        TableHead,
        TableHeader,
        TableRow,
    } from "$lib/components/ui/table";
    import {
        Calendar,
        MessageSquare,
        Home,
        LayoutGrid,
        List,
        Mail,
        Phone,
        Clock,
    } from "lucide-svelte";
    import { Skeleton } from "$lib/components/ui/skeleton";

    let appointments: any[] = [];
    let requests: any[] = [];
    let inquiries: any[] = [];
    let loading = true;
    let viewMode: "list" | "grid" = "list";

    onMount(async () => {
        try {
            const [apptRes, reqRes, inqRes] = await Promise.all([
                fetch("http://127.0.0.1:5000/api/admin/appointments"),
                fetch("http://127.0.0.1:5000/api/admin/requests"),
                fetch("http://127.0.0.1:5000/api/admin/inquiries"),
            ]);

            if (apptRes.ok) appointments = await apptRes.json();
            if (reqRes.ok) requests = await reqRes.json();
            if (inqRes.ok) inquiries = await inqRes.json();
        } catch (e) {
            console.error("Failed to fetch data", e);
        } finally {
            loading = false;
        }
    });

    function formatDate(isoString: string) {
        if (!isoString) return "N/A";
        return new Date(isoString).toLocaleString();
    }
</script>

<div class="space-y-8">
    <div>
        <h1 class="text-3xl font-bold tracking-tight">Leads & Requests</h1>
        <p class="text-muted-foreground">
            Manage all your incoming leads, appointments, and inquiries.
        </p>
    </div>

    <Tabs.Root value="appointments" class="w-full">
        <Tabs.List class="grid w-full grid-cols-3 max-w-[600px] mb-8">
            <Tabs.Trigger value="appointments">Appointments</Tabs.Trigger>
            <Tabs.Trigger value="requests">Property Requests</Tabs.Trigger>
            <Tabs.Trigger value="inquiries">Inquiries</Tabs.Trigger>
        </Tabs.List>

        <!-- APPOINTMENTS TAB -->
        <Tabs.Content value="appointments" class="space-y-4">
            <div class="flex justify-between items-center">
                <h2 class="text-xl font-semibold">Scheduled Viewings</h2>
                <div class="flex items-center gap-2 bg-muted p-1 rounded-lg">
                    <Button
                        variant={viewMode === "list" ? "secondary" : "ghost"}
                        size="sm"
                        onclick={() => (viewMode = "list")}
                    >
                        <List class="w-4 h-4" />
                    </Button>
                    <Button
                        variant={viewMode === "grid" ? "secondary" : "ghost"}
                        size="sm"
                        onclick={() => (viewMode = "grid")}
                    >
                        <LayoutGrid class="w-4 h-4" />
                    </Button>
                </div>
            </div>

            {#if loading}
                <div class="space-y-4">
                    <Skeleton class="h-12 w-full" />
                    <Skeleton class="h-12 w-full" />
                    <Skeleton class="h-12 w-full" />
                </div>
            {:else if appointments.length === 0}
                <div class="text-center py-12 border rounded-lg bg-muted/10">
                    <Calendar
                        class="w-12 h-12 mx-auto text-muted-foreground mb-4"
                    />
                    <h3 class="text-lg font-medium">No appointments found</h3>
                </div>
            {:else if viewMode === "list"}
                <div class="border rounded-lg overflow-hidden">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Property</TableHead>
                                <TableHead>User ID</TableHead>
                                <TableHead>Date & Time</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Created At</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {#each appointments as appt}
                                <TableRow>
                                    <TableCell class="font-medium">
                                        <div class="flex items-center gap-3">
                                            {#if appt.property_image}
                                                <img
                                                    src={appt.property_image}
                                                    alt="Prop"
                                                    class="w-10 h-10 rounded object-cover"
                                                />
                                            {/if}
                                            <div class="flex flex-col">
                                                <span
                                                    >{appt.property_title ||
                                                        "Unknown"}</span
                                                >
                                                <span
                                                    class="text-xs text-muted-foreground"
                                                    >ID: {appt.property_id}</span
                                                >
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>{appt.user_id}</TableCell>
                                    <TableCell>
                                        {appt.date} at {appt.time}
                                    </TableCell>
                                    <TableCell>
                                        <Badge
                                            variant={appt.status === "pending"
                                                ? "secondary"
                                                : appt.status === "confirmed"
                                                  ? "default"
                                                  : "outline"}
                                        >
                                            {appt.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell
                                        class="text-muted-foreground text-xs"
                                    >
                                        {formatDate(appt.created_at)}
                                    </TableCell>
                                </TableRow>
                            {/each}
                        </TableBody>
                    </Table>
                </div>
            {:else}
                <!-- GRID VIEW -->
                <div
                    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                    {#each appointments as appt}
                        <Card>
                            <div
                                class="aspect-video w-full overflow-hidden relative"
                            >
                                <img
                                    src={appt.property_image ||
                                        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
                                    alt="Property"
                                    class="w-full h-full object-cover"
                                />
                                <Badge class="absolute top-2 right-2">
                                    {appt.status}
                                </Badge>
                            </div>
                            <CardContent class="p-4 space-y-3">
                                <h3 class="font-bold line-clamp-1">
                                    {appt.property_title || "Unknown Property"}
                                </h3>
                                <div class="space-y-1 text-sm">
                                    <div class="flex items-center gap-2">
                                        <Calendar
                                            class="w-4 h-4 text-muted-foreground"
                                        />
                                        <span>{appt.date} at {appt.time}</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <Clock
                                            class="w-4 h-4 text-muted-foreground"
                                        />
                                        <span
                                            class="text-xs text-muted-foreground"
                                            >Requested: {formatDate(
                                                appt.created_at,
                                            )}</span
                                        >
                                    </div>
                                </div>
                                <div
                                    class="pt-2 border-t text-xs text-muted-foreground"
                                >
                                    User: {appt.user_id}
                                </div>
                            </CardContent>
                        </Card>
                    {/each}
                </div>
            {/if}
        </Tabs.Content>

        <!-- PROPERTY REQUESTS TAB -->
        <Tabs.Content value="requests" class="space-y-4">
            <h2 class="text-xl font-semibold">Dream Home Requests</h2>
            {#if loading}
                <Skeleton class="h-40 w-full" />
            {:else if requests.length === 0}
                <div class="text-center py-12 border rounded-lg bg-muted/10">
                    <Home
                        class="w-12 h-12 mx-auto text-muted-foreground mb-4"
                    />
                    <h3 class="text-lg font-medium">No requests found</h3>
                </div>
            {:else}
                <div class="grid gap-4">
                    {#each requests as req}
                        <Card>
                            <CardContent class="p-6">
                                <div
                                    class="flex justify-between items-start mb-4"
                                >
                                    <div>
                                        <h3 class="font-semibold text-lg">
                                            Request from {req.user_id}
                                        </h3>
                                        <p
                                            class="text-xs text-muted-foreground"
                                        >
                                            {formatDate(req.created_at)}
                                        </p>
                                    </div>
                                    <Badge variant="outline">{req.status}</Badge
                                    >
                                </div>
                                <div
                                    class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm"
                                >
                                    <div class="bg-muted/30 p-3 rounded-lg">
                                        <span
                                            class="text-muted-foreground block text-xs"
                                            >Location</span
                                        >
                                        <span class="font-medium"
                                            >{req.criteria?.location ||
                                                "Any"}</span
                                        >
                                    </div>
                                    <div class="bg-muted/30 p-3 rounded-lg">
                                        <span
                                            class="text-muted-foreground block text-xs"
                                            >Type</span
                                        >
                                        <span class="font-medium"
                                            >{req.criteria?.type || "Any"}</span
                                        >
                                    </div>
                                    <div class="bg-muted/30 p-3 rounded-lg">
                                        <span
                                            class="text-muted-foreground block text-xs"
                                            >Budget</span
                                        >
                                        <span class="font-medium"
                                            >₹{req.criteria?.minPrice} - ₹{req
                                                .criteria?.maxPrice}</span
                                        >
                                    </div>
                                    <div class="bg-muted/30 p-3 rounded-lg">
                                        <span
                                            class="text-muted-foreground block text-xs"
                                            >Bedrooms</span
                                        >
                                        <span class="font-medium"
                                            >{req.criteria?.bedrooms ||
                                                "Any"}</span
                                        >
                                    </div>
                                </div>
                                {#if req.criteria?.additionalRequirements}
                                    <div
                                        class="mt-4 text-sm bg-muted/10 p-3 rounded-lg"
                                    >
                                        <span class="font-semibold">Note:</span>
                                        {req.criteria.additionalRequirements}
                                    </div>
                                {/if}
                            </CardContent>
                        </Card>
                    {/each}
                </div>
            {/if}
        </Tabs.Content>

        <!-- INQUIRIES TAB -->
        <Tabs.Content value="inquiries" class="space-y-4">
            <h2 class="text-xl font-semibold">Contact Inquiries</h2>
            {#if loading}
                <Skeleton class="h-40 w-full" />
            {:else if inquiries.length === 0}
                <div class="text-center py-12 border rounded-lg bg-muted/10">
                    <MessageSquare
                        class="w-12 h-12 mx-auto text-muted-foreground mb-4"
                    />
                    <h3 class="text-lg font-medium">No inquiries found</h3>
                </div>
            {:else}
                <div class="grid gap-4">
                    {#each inquiries as inq}
                        <Card>
                            <CardContent class="p-6">
                                <div class="flex flex-col md:flex-row gap-6">
                                    <div class="flex-1 space-y-4">
                                        <div
                                            class="flex justify-between items-start"
                                        >
                                            <div>
                                                <h3
                                                    class="font-semibold text-lg"
                                                >
                                                    {inq.subject ||
                                                        "No Subject"}
                                                </h3>
                                                <div
                                                    class="flex items-center gap-4 text-sm text-muted-foreground mt-1"
                                                >
                                                    <span
                                                        class="flex items-center gap-1"
                                                    >
                                                        <Mail class="w-3 h-3" />
                                                        {inq.email}
                                                    </span>
                                                    {#if inq.name}
                                                        <span
                                                            class="flex items-center gap-1"
                                                        >
                                                            User: {inq.name}
                                                        </span>
                                                    {/if}
                                                </div>
                                            </div>
                                            <span
                                                class="text-xs text-muted-foreground"
                                            >
                                                {formatDate(inq.timestamp)}
                                            </span>
                                        </div>

                                        <div
                                            class="bg-muted/30 p-4 rounded-lg text-sm"
                                        >
                                            {inq.message}
                                        </div>

                                        {#if inq.property_id}
                                            <div
                                                class="flex items-center gap-2 text-sm"
                                            >
                                                <Home
                                                    class="w-4 h-4 text-primary"
                                                />
                                                <span class="font-medium"
                                                    >Regarding Property:</span
                                                >
                                                <a
                                                    href="/properties/{inq.property_id}"
                                                    class="text-primary hover:underline"
                                                >
                                                    {inq.property_title ||
                                                        inq.property_id}
                                                </a>
                                            </div>
                                        {/if}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    {/each}
                </div>
            {/if}
        </Tabs.Content>
    </Tabs.Root>
</div>
