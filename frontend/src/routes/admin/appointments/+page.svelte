<script lang="ts">
    import { onMount } from "svelte";
    import { Calendar } from "$lib/components/ui/calendar";
    import * as Table from "$lib/components/ui/table";
    import * as Card from "$lib/components/ui/card";
    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { toast } from "svelte-sonner";
    import { format, parseISO, isSameDay } from "date-fns";
    import {
        Calendar as CalendarIcon,
        List,
        Clock,
        CheckCircle,
        XCircle,
        AlertCircle,
        Loader2,
    } from "lucide-svelte";
    import {
        type DateValue,
        getLocalTimeZone,
        today,
    } from "@internationalized/date";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let appointments: any[] = [];
    let loading = true;
    let viewMode: "list" | "calendar" = "list";
    let value: DateValue | undefined = undefined; // Selected date in calendar
    let selectedAppointment: any = null;
    let isDialogOpen = false;
    let isRescheduleOpen = false;
    let rescheduleDate = "";
    let rescheduleTime = "";
    let processing = false;

    onMount(async () => {
        await fetchAppointments();
    });

    async function fetchAppointments() {
        loading = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/appointments`,
            );
            if (res.ok) {
                appointments = await res.json();
            } else {
                toast.error("Failed to fetch appointments");
            }
        } catch (e) {
            toast.error("Error fetching appointments");
        } finally {
            loading = false;
        }
    }

    async function updateStatus(status: string) {
        if (!selectedAppointment) return;
        processing = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/appointments/${selectedAppointment.id}/status`,
                {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ status }),
                },
            );

            if (res.ok) {
                toast.success(`Appointment marked as ${status}`);
                selectedAppointment.status = status;
                appointments = appointments.map((a) =>
                    a.id === selectedAppointment.id ? { ...a, status } : a,
                );
                isDialogOpen = false;
            } else {
                toast.error("Failed to update status");
            }
        } catch (e) {
            toast.error("Error updating status");
        } finally {
            processing = false;
        }
    }

    async function handleReschedule() {
        if (!selectedAppointment || !rescheduleDate || !rescheduleTime) {
            toast.error("Please select date and time");
            return;
        }
        processing = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/appointments/${selectedAppointment.id}/reschedule`,
                {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        date: rescheduleDate,
                        time: rescheduleTime,
                    }),
                },
            );

            if (res.ok) {
                toast.success("Appointment rescheduled");
                appointments = appointments.map((a) =>
                    a.id === selectedAppointment.id
                        ? {
                              ...a,
                              date: rescheduleDate,
                              time: rescheduleTime,
                              status: "confirmed",
                          }
                        : a,
                );
                isRescheduleOpen = false;
                isDialogOpen = false;
            } else {
                toast.error("Failed to reschedule");
            }
        } catch (e) {
            toast.error("Error rescheduling");
        } finally {
            processing = false;
        }
    }

    function openDetails(appt: any) {
        selectedAppointment = appt;
        isDialogOpen = true;
    }

    function getStatusColor(status: string) {
        switch (status) {
            case "confirmed":
                return "bg-green-500 hover:bg-green-600";
            case "pending":
                return "bg-yellow-500 hover:bg-yellow-600";
            case "cancelled":
                return "bg-red-500 hover:bg-red-600";
            case "completed":
                return "bg-blue-500 hover:bg-blue-600";
            default:
                return "bg-gray-500";
        }
    }

    $: filteredAppointments = value
        ? appointments.filter((a) => a.date === value?.toString())
        : appointments;
</script>

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">Appointments</h2>
            <p class="text-muted-foreground">
                Manage property viewings and meetings.
            </p>
        </div>
        <div class="flex items-center gap-2">
            <Button
                variant={viewMode === "list" ? "default" : "outline"}
                size="icon"
                onclick={() => (viewMode = "list")}
            >
                <List class="h-4 w-4" />
            </Button>
            <Button
                variant={viewMode === "calendar" ? "default" : "outline"}
                size="icon"
                onclick={() => (viewMode = "calendar")}
            >
                <CalendarIcon class="h-4 w-4" />
            </Button>
        </div>
    </div>

    {#if loading}
        <div class="flex justify-center py-8">
            <Loader2 class="h-8 w-8 animate-spin text-primary" />
        </div>
    {:else if viewMode === "list"}
        <Card.Root>
            <Card.Content class="p-0">
                <Table.Root>
                    <Table.Header>
                        <Table.Row>
                            <Table.Head>Property</Table.Head>
                            <Table.Head>User</Table.Head>
                            <Table.Head>Date & Time</Table.Head>
                            <Table.Head>Status</Table.Head>
                            <Table.Head class="text-right">Actions</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each appointments as appt}
                            <Table.Row>
                                <Table.Cell class="font-medium">
                                    <div class="flex items-center gap-2">
                                        {#if appt.property_image}
                                            <img
                                                src={appt.property_image}
                                                alt={appt.property_title}
                                                class="h-8 w-8 rounded object-cover"
                                            />
                                        {/if}
                                        <span class="truncate max-w-[200px]"
                                            >{appt.property_title}</span
                                        >
                                    </div>
                                </Table.Cell>
                                <Table.Cell>{appt.user_id}</Table.Cell>
                                <!-- Ideally fetch user name -->
                                <Table.Cell>
                                    <div class="flex flex-col">
                                        <span>{appt.date}</span>
                                        <span
                                            class="text-xs text-muted-foreground"
                                            >{appt.time}</span
                                        >
                                    </div>
                                </Table.Cell>
                                <Table.Cell>
                                    <Badge class={getStatusColor(appt.status)}
                                        >{appt.status}</Badge
                                    >
                                </Table.Cell>
                                <Table.Cell class="text-right">
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onclick={() => openDetails(appt)}
                                        >View</Button
                                    >
                                </Table.Cell>
                            </Table.Row>
                        {/each}
                        {#if appointments.length === 0}
                            <Table.Row>
                                <Table.Cell
                                    colspan={5}
                                    class="text-center py-8 text-muted-foreground"
                                >
                                    No appointments found.
                                </Table.Cell>
                            </Table.Row>
                        {/if}
                    </Table.Body>
                </Table.Root>
            </Card.Content>
        </Card.Root>
    {:else}
        <div class="grid gap-6 md:grid-cols-[300px_1fr]">
            <Card.Root>
                <Card.Content class="p-4">
                    <Calendar
                        type="single"
                        bind:value
                        class="rounded-md border"
                    />
                </Card.Content>
            </Card.Root>

            <Card.Root>
                <Card.Header>
                    <Card.Title>
                        {value
                            ? format(parseISO(value.toString()), "MMMM d, yyyy")
                            : "All Appointments"}
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <div class="space-y-4">
                        {#each filteredAppointments as appt}
                            <div
                                class="flex items-center justify-between rounded-lg border p-4"
                            >
                                <div class="flex items-center gap-4">
                                    {#if appt.property_image}
                                        <img
                                            src={appt.property_image}
                                            alt={appt.property_title}
                                            class="h-12 w-12 rounded object-cover"
                                        />
                                    {/if}
                                    <div>
                                        <h4 class="font-semibold">
                                            {appt.property_title}
                                        </h4>
                                        <div
                                            class="flex items-center gap-2 text-sm text-muted-foreground"
                                        >
                                            <Clock class="h-3 w-3" />
                                            {appt.time}
                                        </div>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2">
                                    <Badge class={getStatusColor(appt.status)}
                                        >{appt.status}</Badge
                                    >
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onclick={() => openDetails(appt)}
                                        >View</Button
                                    >
                                </div>
                            </div>
                        {/each}
                        {#if filteredAppointments.length === 0}
                            <div class="text-center py-8 text-muted-foreground">
                                No appointments for this date.
                            </div>
                        {/if}
                    </div>
                </Card.Content>
            </Card.Root>
        </div>
    {/if}

    <!-- Details Dialog -->
    <Dialog.Root bind:open={isDialogOpen}>
        <Dialog.Content>
            <Dialog.Header>
                <Dialog.Title>Appointment Details</Dialog.Title>
            </Dialog.Header>
            {#if selectedAppointment}
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <Label class="text-muted-foreground">Property</Label
                            >
                            <p class="font-medium">
                                {selectedAppointment.property_title}
                            </p>
                        </div>
                        <div>
                            <Label class="text-muted-foreground">Status</Label>
                            <div>
                                <Badge
                                    class={getStatusColor(
                                        selectedAppointment.status,
                                    )}>{selectedAppointment.status}</Badge
                                >
                            </div>
                        </div>
                        <div>
                            <Label class="text-muted-foreground">Date</Label>
                            <p class="font-medium">
                                {selectedAppointment.date}
                            </p>
                        </div>
                        <div>
                            <Label class="text-muted-foreground">Time</Label>
                            <p class="font-medium">
                                {selectedAppointment.time}
                            </p>
                        </div>
                    </div>

                    <div class="flex flex-col gap-2 pt-4">
                        {#if selectedAppointment.status === "pending"}
                            <Button
                                class="w-full bg-green-600 hover:bg-green-700"
                                onclick={() => updateStatus("confirmed")}
                                disabled={processing}
                            >
                                <CheckCircle class="mr-2 h-4 w-4" /> Confirm Appointment
                            </Button>
                        {/if}

                        {#if selectedAppointment.status === "confirmed"}
                            <Button
                                class="w-full bg-blue-600 hover:bg-blue-700"
                                onclick={() => updateStatus("completed")}
                                disabled={processing}
                            >
                                <CheckCircle class="mr-2 h-4 w-4" /> Mark as Completed
                            </Button>
                        {/if}

                        <Button
                            variant="outline"
                            class="w-full"
                            onclick={() => (isRescheduleOpen = true)}
                            disabled={processing}
                        >
                            <Clock class="mr-2 h-4 w-4" /> Reschedule
                        </Button>

                        {#if selectedAppointment.status !== "cancelled" && selectedAppointment.status !== "completed"}
                            <Button
                                variant="destructive"
                                class="w-full"
                                onclick={() => updateStatus("cancelled")}
                                disabled={processing}
                            >
                                <XCircle class="mr-2 h-4 w-4" /> Cancel Appointment
                            </Button>
                        {/if}
                    </div>
                </div>
            {/if}
        </Dialog.Content>
    </Dialog.Root>

    <!-- Reschedule Dialog -->
    <Dialog.Root bind:open={isRescheduleOpen}>
        <Dialog.Content>
            <Dialog.Header>
                <Dialog.Title>Reschedule Appointment</Dialog.Title>
            </Dialog.Header>
            <div class="space-y-4 py-4">
                <div class="space-y-2">
                    <Label>New Date</Label>
                    <Input type="date" bind:value={rescheduleDate} />
                </div>
                <div class="space-y-2">
                    <Label>New Time</Label>
                    <Input type="time" bind:value={rescheduleTime} />
                </div>
                <Button
                    class="w-full"
                    onclick={handleReschedule}
                    disabled={processing}
                >
                    {processing ? "Updating..." : "Confirm Reschedule"}
                </Button>
            </div>
        </Dialog.Content>
    </Dialog.Root>
</div>
