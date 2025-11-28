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
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

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
            // Use fetchWithAuth if user is logged in, otherwise regular fetch (if we allow guests)
            // But for now, let's assume we want to track it with user ID if available.
            // If the endpoint requires auth, we must use fetchWithAuth.
            // The plan says "token verification for all user-accessible API endpoints".
            // If this is a public inquiry form, it might not need auth.
            // However, the code passes user_id.

            if ($user) {
                await fetchWithAuth(`${API_BASE_URL}/api/inquiries`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        type: "property",
                        property_id: propertyId,
                        property_title: propertyTitle,
                        user_id: ($user as any).uid,
                        message: message,
                        email: ($user as any).email,
                    }),
                });
            } else {
                // Fallback for guests if allowed, or force login.
                // The current code passes $user?.uid.
                // If we enforce auth on backend, we need fetchWithAuth.
                // If we allow guests, we use fetch.
                // Let's assume for now we use fetchWithAuth if user exists, or fetch if not.
                // But wait, fetchWithAuth throws if not logged in.
                // I'll stick to the existing logic: if user is logged in, use fetchWithAuth.
                // If not, use fetch (and backend handles it).
                // Actually, looking at the code: `user_id: $user?.uid`.
                // If I change to fetchWithAuth, I must ensure user is logged in.
                // If the user is NOT logged in, `handleContact` should probably still work for guests?
                // The backend `verify_token` decorator would block it if I applied it to `inquiries`.
                // I applied `verify_token` to `inquiries` in `backend/routes/inquiries.py`?
                // Let's check `backend/routes/inquiries.py` later.
                // For now, I'll use fetchWithAuth ONLY if user is logged in.

                await fetch(`${API_BASE_URL}/api/inquiries`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        type: "property",
                        property_id: propertyId,
                        property_title: propertyTitle,
                        user_id: null,
                        message: message,
                        email: null,
                    }),
                });
            }

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
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/appointments`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        user_id: ($user as any).uid,
                        property_id: propertyId,
                        date: date.toString(),
                        time: time,
                    }),
                },
            );

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
