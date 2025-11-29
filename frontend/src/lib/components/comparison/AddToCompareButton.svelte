<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { ArrowLeftRight, Check } from "lucide-svelte";
    import { comparison } from "$lib/stores/comparison";
    import { cn } from "$lib/utils";

    export let propertyId: string;
    export let variant: "default" | "outline" | "ghost" | "secondary" =
        "outline";
    export let size: "default" | "sm" | "lg" | "icon" = "default";
    export let className: string = "";

    export let showText = true;

    $: isSelected = $comparison.includes(propertyId);

    function toggle(e?: MouseEvent) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        comparison.toggleProperty(propertyId);
    }
</script>

<Button
    {variant}
    {size}
    class={cn(
        isSelected &&
            "bg-primary/10 text-primary border-primary/50 hover:bg-primary/20",
        className,
    )}
    onclick={toggle}
    title={isSelected ? "Remove from comparison" : "Add to comparison"}
    aria-label={isSelected ? "Remove from comparison" : "Add to comparison"}
>
    {#if isSelected}
        <Check class={cn("h-4 w-4", showText && "mr-2")} />
        {#if showText}
            <span class="hidden sm:inline">Added</span>
        {/if}
    {:else}
        <ArrowLeftRight class={cn("h-4 w-4", showText && "mr-2")} />
        {#if showText}
            <span class="hidden sm:inline">Compare</span>
        {/if}
    {/if}
</Button>
