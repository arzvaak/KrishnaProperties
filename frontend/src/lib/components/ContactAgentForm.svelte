<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import {
        CheckCircle2,
        Mail,
        Calendar as CalendarIcon,
        Phone,
    } from "lucide-svelte";
    import * as Popover from "$lib/components/ui/popover";
    import { Calendar } from "$lib/components/ui/calendar";
    import { user } from "$lib/stores/auth";
    import { toast } from "svelte-sonner";
    import type { DateValue } from "@internationalized/date";

    export let propertyId: string;
    export let propertyTitle: string;

    let message = "";
    let contactSent = false;
    let date: DateValue | undefined = undefined;
    let time = "10:00";
    let isScheduleOpen = false;
    let scheduling = false;

    async function handleContact() {
        try {
            await fetch("http://127.0.0.1:5000/api/analytics/track", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    type: "contact",
                    property_id: propertyId,
                    user_id: $user?.uid,
                    metadata: { message },
                }),
            });
            contactSent = true;
            toast.success("Message sent to team!");
            message = "";
        } catch (e) {
            toast.error("Failed to send message");
        }
    }

    async function handleSchedule() {
        if (!$user) {
            toast.error("Please login to schedule a viewing");
            return;
        }
        if (!date) {
            toast.error("Please select a date");
            return;
        }

        scheduling = true;
        try {
            const res = await fetch("http://127.0.0.1:5000/api/appointments", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: $user.uid,
                    property_id: propertyId,
                    date: date.toString(),
                    time: time,
                }),
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Failed to schedule");

            toast.success(data.message);
            isScheduleOpen = false;
        } catch (e: any) {
            toast.error(e.message);
        } finally {
            scheduling = false;
        }
    }
</script>

<Card class="border-none shadow-xl bg-card/95 backdrop-blur-sm">
    <CardHeader class="bg-primary/5 pb-6">
        <CardTitle class="text-xl">Interested in this property?</CardTitle>
        <p class="text-sm text-muted-foreground">
            Our premium agents are ready to help you.
        </p>
    </CardHeader>
    <CardContent class="p-6 space-y-4">
        {#if contactSent}
            <div
                class="bg-green-50 text-green-700 p-6 rounded-xl text-center border border-green-100"
            >
                <CheckCircle2 class="w-12 h-12 mx-auto mb-2 text-green-600" />
                <p class="font-bold">Message Sent!</p>
                <p class="text-sm mt-1">We will contact you shortly.</p>
            </div>
        {:else}
            <div class="space-y-3">
                <textarea
                    class="flex min-h-[120px] w-full rounded-xl border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none"
                    placeholder="Hi, I am interested in {propertyTitle}..."
                    bind:value={message}
                ></textarea>
                <Button
                    class="w-full h-12 text-base font-semibold shadow-lg hover:shadow-xl transition-all"
                    onclick={handleContact}
                    disabled={!message}
                >
                    <Mail class="w-4 h-4 mr-2" /> Send Message
                </Button>
            </div>
        {/if}

        <div class="relative py-2">
            <div class="absolute inset-0 flex items-center">
                <span class="w-full border-t"></span>
            </div>
            <div class="relative flex justify-center text-xs uppercase">
                <span class="bg-card px-2 text-muted-foreground">Or</span>
            </div>
        </div>

        <Popover.Root bind:open={isScheduleOpen}>
            <Popover.Trigger class="w-full">
                <Button
                    variant="outline"
                    class="w-full h-12 border-primary/20 hover:bg-primary/5 hover:text-primary hover:border-primary/50"
                >
                    <CalendarIcon class="w-4 h-4 mr-2" /> Schedule Viewing
                </Button>
            </Popover.Trigger>
            <Popover.Content class="w-auto p-0" align="end">
                <div class="p-4 space-y-4">
                    <div class="space-y-2">
                        <h4 class="font-medium leading-none">Pick a date</h4>
                        <Calendar
                            bind:value={date}
                            type="single"
                            class="rounded-md border"
                        />
                    </div>
                    <div class="space-y-2">
                        <h4 class="font-medium leading-none">Pick a time</h4>
                        <select
                            bind:value={time}
                            class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                        >
                            <option value="10:00">10:00 AM</option>
                            <option value="11:00">11:00 AM</option>
                            <option value="12:00">12:00 PM</option>
                            <option value="13:00">01:00 PM</option>
                            <option value="14:00">02:00 PM</option>
                            <option value="15:00">03:00 PM</option>
                            <option value="16:00">04:00 PM</option>
                            <option value="17:00">05:00 PM</option>
                        </select>
                    </div>
                    <Button
                        class="w-full"
                        onclick={handleSchedule}
                        disabled={scheduling}
                    >
                        {scheduling ? "Scheduling..." : "Confirm Booking"}
                    </Button>
                </div>
            </Popover.Content>
        </Popover.Root>

        <Button variant="outline" class="w-full h-12" href="tel:+919876543210">
            <Phone class="w-4 h-4 mr-2" /> Call Agent
        </Button>
    </CardContent>
</Card>
