<script>
    import { Button } from "$lib/components/ui/button";
    import { ShieldAlert, Home, ArrowLeft } from "lucide-svelte";
</script>

<div
    class="min-h-screen flex flex-col items-center justify-center bg-background p-4"
>
    <div class="max-w-md w-full text-center space-y-6">
        <div class="flex justify-center">
            <div class="p-4 bg-destructive/10 rounded-full">
                <ShieldAlert class="h-16 w-16 text-destructive" />
            </div>
        </div>

        <div class="space-y-2">
            <h1 class="text-3xl font-bold tracking-tighter sm:text-4xl">
                Access Denied
            </h1>
            <p class="text-muted-foreground">
                You do not have permission to view this page. This area is
                restricted to administrators only.
            </p>
        </div>

        <div class="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Button variant="outline" href="/">
                <Home class="mr-2 h-4 w-4" />
                Go Home
            </Button>
            <Button href="/login">
                <ArrowLeft class="mr-2 h-4 w-4" />
                Back to Login
            </Button>
        </div>

        <div class="pt-8 text-xs text-muted-foreground">
            <p>Error Code: 403 Forbidden</p>
            <p>IP Address logged for security purposes.</p>
        </div>
    </div>
</div>
