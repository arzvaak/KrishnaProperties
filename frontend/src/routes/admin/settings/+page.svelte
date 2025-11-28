<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";
    import { toast } from "svelte-sonner";
    import { Loader2, Save } from "lucide-svelte";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";
    import * as Tabs from "$lib/components/ui/tabs";

    let loading = false;
    let saving = false;

    let general = { siteName: "", tagline: "", logo: "" };
    let contact = { email: "", phone: "", address: "", mapEmbedUrl: "" };
    let social = {
        facebook: "",
        twitter: "",
        instagram: "",
        linkedin: "",
        youtube: "",
    };
    let seo = { defaultTitle: "", defaultDescription: "", defaultKeywords: "" };
    let emailTemplates: any = {};

    const templateKeys = [
        { key: "saved_search_match", label: "Saved Search Match" },
        { key: "price_drop", label: "Price Drop Alert" },
        { key: "appointment_confirmation", label: "Appointment Confirmation" },
        {
            key: "appointment_status_change",
            label: "Appointment Status Change",
        },
        { key: "appointment_reschedule", label: "Appointment Reschedule" },
        { key: "inquiry_auto_reply", label: "Inquiry Auto-Reply" },
        { key: "request_auto_reply", label: "Dream Home Request Auto-Reply" },
    ];

    onMount(async () => {
        await fetchSettings();
    });

    async function fetchSettings() {
        loading = true;
        try {
            const endpoints = [
                "general",
                "contact",
                "social",
                "seo",
                "email_templates",
            ];
            const promises = endpoints.map((type) =>
                fetchWithAuth(
                    `${API_BASE_URL}/api/admin/settings/${type}`,
                ).then((res) => res.json()),
            );

            const [genData, conData, socData, seoData, emailData] =
                await Promise.all(promises);

            general = { ...general, ...genData };
            contact = { ...contact, ...conData };
            social = { ...social, ...socData };
            seo = { ...seo, ...seoData };

            // Initialize email templates if empty
            templateKeys.forEach((t) => {
                if (!emailData[t.key]) {
                    emailData[t.key] = { subject: "", body: "" };
                }
            });
            emailTemplates = emailData;
        } catch (e) {
            toast.error("Failed to load settings");
        } finally {
            loading = false;
        }
    }

    async function saveSettings(type: string, data: any) {
        saving = true;
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/settings/${type}`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data),
                },
            );

            if (res.ok) {
                toast.success(
                    `${type.charAt(0).toUpperCase() + type.slice(1)} settings saved`,
                );
            } else {
                toast.error("Failed to save settings");
            }
        } catch (e) {
            toast.error("Error saving settings");
        } finally {
            saving = false;
        }
    }
</script>

<div class="container py-6 max-w-4xl">
    <div class="flex items-center justify-between mb-8">
        <div>
            <h1 class="text-3xl font-bold tracking-tight">System Settings</h1>
            <p class="text-muted-foreground">
                Manage global site configuration.
            </p>
        </div>
    </div>

    {#if loading}
        <div class="flex justify-center py-12">
            <Loader2 class="h-8 w-8 animate-spin text-primary" />
        </div>
    {:else}
        <Tabs.Root value="general" class="space-y-6">
            <Tabs.List class="grid w-full grid-cols-5">
                <Tabs.Trigger value="general">General</Tabs.Trigger>
                <Tabs.Trigger value="contact">Contact</Tabs.Trigger>
                <Tabs.Trigger value="social">Social</Tabs.Trigger>
                <Tabs.Trigger value="seo">SEO</Tabs.Trigger>
                <Tabs.Trigger value="email">Email</Tabs.Trigger>
            </Tabs.List>

            <!-- General Settings -->
            <Tabs.Content value="general" class="space-y-6">
                <div class="grid gap-4 bg-card p-6 rounded-lg border">
                    <div class="space-y-2">
                        <Label>Site Name</Label>
                        <Input bind:value={general.siteName} />
                    </div>
                    <div class="space-y-2">
                        <Label>Tagline</Label>
                        <Input bind:value={general.tagline} />
                    </div>
                    <div class="space-y-2">
                        <Label>Logo URL</Label>
                        <Input bind:value={general.logo} />
                    </div>
                    <Button
                        onclick={() => saveSettings("general", general)}
                        disabled={saving}
                    >
                        {#if saving}
                            <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                        {/if} Save Changes
                    </Button>
                </div>
            </Tabs.Content>

            <!-- Contact Settings -->
            <Tabs.Content value="contact" class="space-y-6">
                <div class="grid gap-4 bg-card p-6 rounded-lg border">
                    <div class="space-y-2">
                        <Label>Email Address</Label>
                        <Input bind:value={contact.email} />
                    </div>
                    <div class="space-y-2">
                        <Label>Phone Number</Label>
                        <Input bind:value={contact.phone} />
                    </div>
                    <div class="space-y-2">
                        <Label>Address</Label>
                        <Textarea bind:value={contact.address} />
                    </div>
                    <div class="space-y-2">
                        <Label>Map Embed URL (iframe src)</Label>
                        <Input bind:value={contact.mapEmbedUrl} />
                    </div>
                    <Button
                        onclick={() => saveSettings("contact", contact)}
                        disabled={saving}
                    >
                        {#if saving}
                            <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                        {/if} Save Changes
                    </Button>
                </div>
            </Tabs.Content>

            <!-- Social Settings -->
            <Tabs.Content value="social" class="space-y-6">
                <div class="grid gap-4 bg-card p-6 rounded-lg border">
                    <div class="space-y-2">
                        <Label>Facebook URL</Label>
                        <Input
                            bind:value={social.facebook}
                            placeholder="https://facebook.com/..."
                        />
                    </div>
                    <div class="space-y-2">
                        <Label>Twitter URL</Label>
                        <Input
                            bind:value={social.twitter}
                            placeholder="https://twitter.com/..."
                        />
                    </div>
                    <div class="space-y-2">
                        <Label>Instagram URL</Label>
                        <Input
                            bind:value={social.instagram}
                            placeholder="https://instagram.com/..."
                        />
                    </div>
                    <div class="space-y-2">
                        <Label>LinkedIn URL</Label>
                        <Input
                            bind:value={social.linkedin}
                            placeholder="https://linkedin.com/..."
                        />
                    </div>
                    <div class="space-y-2">
                        <Label>YouTube URL</Label>
                        <Input
                            bind:value={social.youtube}
                            placeholder="https://youtube.com/..."
                        />
                    </div>
                    <Button
                        onclick={() => saveSettings("social", social)}
                        disabled={saving}
                    >
                        {#if saving}
                            <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                        {/if} Save Changes
                    </Button>
                </div>
            </Tabs.Content>

            <!-- SEO Settings -->
            <Tabs.Content value="seo" class="space-y-6">
                <div class="grid gap-4 bg-card p-6 rounded-lg border">
                    <div class="space-y-2">
                        <Label>Default Meta Title</Label>
                        <Input bind:value={seo.defaultTitle} />
                    </div>
                    <div class="space-y-2">
                        <Label>Default Meta Description</Label>
                        <Textarea bind:value={seo.defaultDescription} />
                    </div>
                    <div class="space-y-2">
                        <Label>Default Keywords</Label>
                        <Input
                            bind:value={seo.defaultKeywords}
                            placeholder="comma, separated, keywords"
                        />
                    </div>
                    <Button
                        onclick={() => saveSettings("seo", seo)}
                        disabled={saving}
                    >
                        {#if saving}
                            <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                        {/if} Save Changes
                    </Button>
                </div>
            </Tabs.Content>

            <!-- Email Templates -->
            <Tabs.Content value="email" class="space-y-6">
                <div class="grid gap-8 bg-card p-6 rounded-lg border">
                    {#each templateKeys as t}
                        <div class="space-y-4 border-b pb-6 last:border-0">
                            <h3 class="font-semibold text-lg">{t.label}</h3>
                            <div class="space-y-2">
                                <Label>Subject</Label>
                                <Input
                                    bind:value={emailTemplates[t.key].subject}
                                />
                            </div>
                            <div class="space-y-2">
                                <Label>HTML Body</Label>
                                <p class="text-xs text-muted-foreground">
                                    Supported placeholders depend on the
                                    template type.
                                </p>
                                <Textarea
                                    bind:value={emailTemplates[t.key].body}
                                    class="font-mono min-h-[200px]"
                                />
                            </div>
                        </div>
                    {/each}
                    <Button
                        onclick={() =>
                            saveSettings("email_templates", emailTemplates)}
                        disabled={saving}
                    >
                        {#if saving}
                            <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                        {/if} Save Changes
                    </Button>
                </div>
            </Tabs.Content>
        </Tabs.Root>
    {/if}
</div>
