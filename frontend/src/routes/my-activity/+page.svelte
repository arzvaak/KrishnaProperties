<script lang="ts">
    import { onMount } from "svelte";
    import { user } from "$lib/stores/auth";
    import * as Tabs from "$lib/components/ui/tabs";
    import { Card, CardContent } from "$lib/components/ui/card";
    import { Badge } from "$lib/components/ui/badge";
    import { Button } from "$lib/components/ui/button";
    import { Calendar, MessageSquare, Clock } from "lucide-svelte";

    let inquiries: any[] = [];
    let appointments: any[] = [];
    let loading = true;

    onMount(() => {
        user.subscribe(async (u) => {
            if (u) {
                await Promise.all([
                    fetchInquiries(u.uid),
                    fetchAppointments(u.uid),
                ]);
                loading = false;
            }
        });
    });

    async function fetchInquiries(uid: string) {
        try {
            const res = await fetch(
                `http://127.0.0.1:5000/api/users/${uid}/inquiries`,
            );
            if (res.ok) inquiries = await res.json();
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchAppointments(uid: string) {
        try {
            const res = await fetch(
                `http://127.0.0.1:5000/api/users/${uid}/appointments`,
            );
            if (res.ok) appointments = await res.json();
        } catch (e) {
            console.error(e);
        }
    }
</script>

<div class="container py-10">
    <h1 class="text-3xl font-bold mb-8">My Activity</h1>

    <Tabs.Root value="appointments" class="w-full">
        <Tabs.List class="grid w-full grid-cols-2 max-w-[400px] mb-8">
            <Tabs.Trigger value="appointments">Appointments</Tabs.Trigger>
            <Tabs.Trigger value="inquiries">Inquiries</Tabs.Trigger>
        </Tabs.List>

        <Tabs.Content value="appointments">
            {#if loading}
                <p>Loading...</p>
            {:else if appointments.length === 0}
                <div class="text-center py-12 border rounded-lg bg-muted/10">
                    <Calendar
                        class="w-12 h-12 mx-auto text-muted-foreground mb-4"
                    />
                    <h3 class="text-lg font-medium">No appointments yet</h3>
                    <p class="text-muted-foreground">
                        Schedule a viewing for a property you like!
                    </p>
                    <Button href="/properties" variant="link" class="mt-2"
                        >Browse Properties</Button
                    >
                </div>
            {:else}
                <div class="grid gap-4">
                    {#each appointments as appt}
                        <Card>
                            <CardContent
                                class="p-6 flex flex-col md:flex-row gap-6 items-start"
                            >
                                {#if appt.property_image}
                                    <img
                                        src={appt.property_image}
                                        alt="Property"
                                        class="w-full md:w-32 h-32 object-cover rounded-md"
                                    />
                                {/if}
                                <div class="flex-1 space-y-2">
                                    <div
                                        class="flex justify-between items-start"
                                    >
                                        <h3 class="font-semibold text-lg">
                                            {appt.property_title ||
                                                "Unknown Property"}
                                        </h3>
                                        <Badge
                                            variant={appt.status === "pending"
                                                ? "secondary"
                                                : appt.status === "confirmed"
                                                  ? "default"
                                                  : "outline"}
                                        >
                                            {appt.status
                                                .charAt(0)
                                                .toUpperCase() +
                                                appt.status.slice(1)}
                                        </Badge>
                                    </div>
                                    <div
                                        class="flex items-center text-muted-foreground"
                                    >
                                        <Calendar class="w-4 h-4 mr-2" />
                                        {new Date(
                                            appt.date,
                                        ).toLocaleDateString()} at {appt.time}
                                    </div>
                                    <div class="text-xs text-muted-foreground">
                                        Requested on {new Date(
                                            appt.created_at,
                                        ).toLocaleDateString()}
                                    </div>
                                </div>
                                <Button
                                    variant="outline"
                                    href="/properties/{appt.property_id}"
                                    >View Property</Button
                                >
                            </CardContent>
                        </Card>
                    {/each}
                </div>
            {/if}
        </Tabs.Content>

        <Tabs.Content value="inquiries">
            {#if loading}
                <p>Loading...</p>
            {:else if inquiries.length === 0}
                <div class="text-center py-12 border rounded-lg bg-muted/10">
                    <MessageSquare
                        class="w-12 h-12 mx-auto text-muted-foreground mb-4"
                    />
                    <h3 class="text-lg font-medium">No inquiries yet</h3>
                    <p class="text-muted-foreground">
                        Contact us about properties you're interested in.
                    </p>
                    <Button href="/properties" variant="link" class="mt-2"
                        >Browse Properties</Button
                    >
                </div>
            {:else}
                <div class="grid gap-4">
                    {#each inquiries as inq}
                        <Card>
                            <CardContent
                                class="p-6 flex flex-col md:flex-row gap-6 items-start"
                            >
                                {#if inq.property_image}
                                    <img
                                        src={inq.property_image}
                                        alt="Property"
                                        class="w-full md:w-32 h-32 object-cover rounded-md"
                                    />
                                {/if}
                                <div class="flex-1 space-y-2">
                                    <h3 class="font-semibold text-lg">
                                        {inq.property_title ||
                                            "General Inquiry"}
                                    </h3>
                                    <div
                                        class="bg-muted p-3 rounded-md text-sm"
                                    >
                                        "{inq.metadata?.message ||
                                            "No message content"}"
                                    </div>
                                    <div
                                        class="flex items-center text-xs text-muted-foreground"
                                    >
                                        <Clock class="w-3 h-3 mr-1" />
                                        Sent on {new Date(
                                            inq.timestamp,
                                        ).toLocaleDateString()}
                                    </div>
                                </div>
                                <Button
                                    variant="outline"
                                    href="/properties/{inq.property_id}"
                                    >View Property</Button
                                >
                            </CardContent>
                        </Card>
                    {/each}
                </div>
            {/if}
        </Tabs.Content>
    </Tabs.Root>
</div>
