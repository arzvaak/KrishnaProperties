<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
        CardDescription,
    } from "$lib/components/ui/card";
    import { toast } from "svelte-sonner";
    import { Mail, Phone, MapPin } from "lucide-svelte";

    let loading = false;
    let name = "";
    let email = "";
    let subject = "";
    let message = "";

    async function handleSubmit() {
        loading = true;
        try {
            // 1. Track the contact event
            await fetch("http://127.0.0.1:5000/api/analytics/track", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    type: "contact",
                    metadata: { name, email, subject, message },
                }),
            });

            // 2. Simulate sending email (or implement actual email API here)
            await new Promise((resolve) => setTimeout(resolve, 1000));

            toast.success(
                "Message sent successfully! We will get back to you soon.",
            );
            name = "";
            email = "";
            subject = "";
            message = "";
        } catch (error) {
            console.error(error);
            toast.error("Failed to send message. Please try again.");
        } finally {
            loading = false;
        }
    }
</script>

<div class="container py-12">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Contact Info -->
        <div class="space-y-8">
            <div>
                <h1 class="text-4xl font-bold mb-4">Get in Touch</h1>
                <p class="text-muted-foreground text-lg">
                    Have questions about a property or need help finding your
                    dream home? We're here to help.
                </p>
            </div>

            <div class="space-y-6">
                <div class="flex items-start gap-4">
                    <div class="bg-primary/10 p-3 rounded-lg">
                        <Phone class="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <h3 class="font-semibold mb-1">Phone</h3>
                        <p class="text-muted-foreground">+91 98765 43210</p>
                        <p class="text-muted-foreground">+91 12345 67890</p>
                    </div>
                </div>

                <div class="flex items-start gap-4">
                    <div class="bg-primary/10 p-3 rounded-lg">
                        <Mail class="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <h3 class="font-semibold mb-1">Email</h3>
                        <p class="text-muted-foreground">
                            hello@krishnarealestate.com
                        </p>
                        <p class="text-muted-foreground">
                            support@krishnarealestate.com
                        </p>
                    </div>
                </div>

                <div class="flex items-start gap-4">
                    <div class="bg-primary/10 p-3 rounded-lg">
                        <MapPin class="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <h3 class="font-semibold mb-1">Office</h3>
                        <p class="text-muted-foreground">
                            123 Real Estate Tower, <br />
                            Bandra West, Mumbai, <br />
                            Maharashtra 400050
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contact Form -->
        <Card>
            <CardHeader>
                <CardTitle>Send us a Message</CardTitle>
                <CardDescription
                    >Fill out the form below and we'll respond within 24 hours.</CardDescription
                >
            </CardHeader>
            <CardContent class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="name">Name</Label>
                        <Input
                            id="name"
                            placeholder="John Doe"
                            bind:value={name}
                        />
                    </div>
                    <div class="space-y-2">
                        <Label for="email">Email</Label>
                        <Input
                            id="email"
                            type="email"
                            placeholder="john@example.com"
                            bind:value={email}
                        />
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="subject">Subject</Label>
                    <Input
                        id="subject"
                        placeholder="Inquiry about..."
                        bind:value={subject}
                    />
                </div>

                <div class="space-y-2">
                    <Label for="message">Message</Label>
                    <Textarea
                        id="message"
                        placeholder="How can we help you?"
                        class="min-h-[150px]"
                        bind:value={message}
                    />
                </div>

                <Button
                    class="w-full"
                    onclick={handleSubmit}
                    disabled={loading || !name || !email || !message}
                >
                    {loading ? "Sending..." : "Send Message"}
                </Button>
            </CardContent>
        </Card>
    </div>
</div>
