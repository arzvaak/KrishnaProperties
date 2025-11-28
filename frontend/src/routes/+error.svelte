<script lang="ts">
    import { page } from "$app/stores";
    import { Button } from "$lib/components/ui/button";
    import { AlertTriangle } from "lucide-svelte";
</script>

<div
    class="min-h-[80vh] flex flex-col items-center justify-center text-center px-4"
>
    <div
        class="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mb-6"
    >
        <AlertTriangle class="w-12 h-12 text-red-500" />
    </div>

    <h1 class="text-4xl font-bold mb-2">
        {$page.status}: {$page.error?.message || "Something went wrong"}
    </h1>

    <p class="text-muted-foreground text-lg max-w-md mb-8">
        We apologize for the inconvenience. The page you are looking for might
        have been removed or is temporarily unavailable.
    </p>

    <div class="flex gap-4">
        <Button variant="outline" onclick={() => history.back()}>Go Back</Button
        >
        <Button href="/">Return Home</Button>
    </div>
</div>
