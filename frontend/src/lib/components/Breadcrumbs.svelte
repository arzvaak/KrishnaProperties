<script lang="ts">
    import { page } from "$app/stores";
    import { ChevronRight, Home } from "lucide-svelte";

    $: crumbs = $page.url.pathname
        .split("/")
        .filter((c) => c !== "")
        .map((c, i, arr) => {
            const path = "/" + arr.slice(0, i + 1).join("/");
            const label =
                c.charAt(0).toUpperCase() + c.slice(1).replace(/-/g, " ");
            return { path, label };
        });
</script>

{#if crumbs.length > 0}
    <nav
        aria-label="Breadcrumb"
        class="flex items-center text-sm text-muted-foreground mb-6 overflow-x-auto whitespace-nowrap"
    >
        <a
            href="/"
            class="flex items-center hover:text-primary transition-colors"
        >
            <Home class="w-4 h-4" />
        </a>
        {#each crumbs as crumb, i}
            <ChevronRight class="w-4 h-4 mx-2 flex-shrink-0" />
            {#if i === crumbs.length - 1}
                <span class="font-medium text-foreground">{crumb.label}</span>
            {:else}
                <a
                    href={crumb.path}
                    class="hover:text-primary transition-colors"
                >
                    {crumb.label}
                </a>
            {/if}
        {/each}
    </nav>
{/if}
