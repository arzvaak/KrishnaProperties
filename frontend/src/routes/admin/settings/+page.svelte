<script lang="ts">
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
        CardDescription,
    } from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Switch } from "$lib/components/ui/switch";
    import { Separator } from "$lib/components/ui/separator";
    import { toast } from "svelte-sonner";

    let settings = {
        siteName: "Krishna Real Estate",
        maintenanceMode: false,
        allowRegistration: true,
        contactEmail: "admin@krishnarealestate.com",
    };

    let saving = false;

    async function saveSettings() {
        saving = true;
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 1000));
        toast.success("Settings saved successfully");
        saving = false;
    }
</script>

<div class="space-y-6 max-w-4xl">
    <div>
        <h1 class="text-3xl font-bold tracking-tight">Settings</h1>
        <p class="text-muted-foreground">Manage system-wide configurations.</p>
    </div>

    <div class="grid gap-6">
        <Card>
            <CardHeader>
                <CardTitle>General Settings</CardTitle>
                <CardDescription
                    >Basic configuration for the website.</CardDescription
                >
            </CardHeader>
            <CardContent class="space-y-4">
                <div class="space-y-2">
                    <Label for="siteName">Site Name</Label>
                    <Input id="siteName" bind:value={settings.siteName} />
                </div>
                <div class="space-y-2">
                    <Label for="contactEmail">Contact Email</Label>
                    <Input
                        id="contactEmail"
                        bind:value={settings.contactEmail}
                    />
                </div>
            </CardContent>
        </Card>

        <Card>
            <CardHeader>
                <CardTitle>Access Control</CardTitle>
                <CardDescription
                    >Manage user access and site availability.</CardDescription
                >
            </CardHeader>
            <CardContent class="space-y-6">
                <div class="flex items-center justify-between space-x-2">
                    <div class="space-y-0.5">
                        <Label class="text-base">Maintenance Mode</Label>
                        <p class="text-sm text-muted-foreground">
                            Disable public access to the site.
                        </p>
                    </div>
                    <Switch bind:checked={settings.maintenanceMode} />
                </div>
                <Separator />
                <div class="flex items-center justify-between space-x-2">
                    <div class="space-y-0.5">
                        <Label class="text-base">Allow Registration</Label>
                        <p class="text-sm text-muted-foreground">
                            Allow new users to sign up.
                        </p>
                    </div>
                    <Switch bind:checked={settings.allowRegistration} />
                </div>
            </CardContent>
        </Card>

        <div class="flex justify-end">
            <Button onclick={saveSettings} disabled={saving}>
                {saving ? "Saving..." : "Save Settings"}
            </Button>
        </div>
    </div>

    <div class="mt-10">
        <h2 class="text-2xl font-bold tracking-tight mb-4">Role Management</h2>
        <p class="text-muted-foreground mb-6">
            Manage administrators and team members.
        </p>

        <Card>
            <CardHeader>
                <CardTitle>Team Members</CardTitle>
                <CardDescription
                    >Users with elevated privileges.</CardDescription
                >
            </CardHeader>
            <CardContent>
                <div class="space-y-4">
                    <p class="text-sm text-muted-foreground">
                        To assign roles, go to the <a
                            href="/admin/users"
                            class="text-primary hover:underline">Users</a
                        > page, select a user, and use the "Role Management" section
                        in their profile.
                    </p>
                    <Button variant="outline" href="/admin/users"
                        >Manage Users & Roles</Button
                    >
                </div>
            </CardContent>
        </Card>
    </div>
</div>
