<script lang="ts">
    import { comparison } from "$lib/stores/comparison";
    import { Button } from "$lib/components/ui/button";
    import { X, ArrowRight } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";
    import { goto } from "$app/navigation";

    $: count = $comparison.length;

    function clear() {
        comparison.clear();
    }
</script>

{#if count > 0}
    <div
        transition:fly={{ y: 100, duration: 300 }}
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 w-full max-w-md px-4"
    >
        <div
            class="bg-background/80 backdrop-blur-md border border-border shadow-2xl rounded-full p-2 pl-6 flex items-center justify-between gap-4"
        >
            <div class="flex items-center gap-2">
                <span class="font-semibold text-sm">
                    {count}
                    {count === 1 ? "property" : "properties"} selected
                </span>
                <button
                    class="text-xs text-muted-foreground hover:text-foreground underline"
                    onclick={clear}
                >
                    Clear
                </button>
            </div>

            <Button size="sm" class="rounded-full px-6" href="/compare">
                Compare Now <ArrowRight class="ml-2 h-3 w-3" />
            </Button>
        </div>
    </div>
{/if}
