<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { Loader2, Mail, Download, Globe, User } from "lucide-svelte";
    import {
        fetchLeads,
        updateLeadStatus,
        exportLeads,
        type Lead,
    } from "$lib/services/leads";
    import { toast } from "svelte-sonner";

    let leads: Lead[] = [];
    let loading = true;
    let draggingLead: Lead | null = null;
    let exporting = false;

    const columns = [
        { id: "new", label: "New", color: "bg-blue-100 text-blue-800" },
        {
            id: "contacted",
            label: "Contacted",
            color: "bg-yellow-100 text-yellow-800",
        },
        {
            id: "qualified",
            label: "Qualified",
            color: "bg-purple-100 text-purple-800",
        },
        {
            id: "converted",
            label: "Converted",
            color: "bg-green-100 text-green-800",
        },
        { id: "lost", label: "Lost", color: "bg-gray-100 text-gray-800" },
    ];

    onMount(async () => {
        await loadLeads();
    });

    async function loadLeads() {
        loading = true;
        leads = await fetchLeads();
        loading = false;
    }

    async function handleExport() {
        exporting = true;
        await exportLeads();
        exporting = false;
    }

    async function handleStatusUpdate(lead: Lead, newStatus: string) {
        const originalStatus = lead.status;
        // Optimistic update
        leads = leads.map((l) =>
            l.id === lead.id ? { ...l, status: newStatus } : l,
        );

        const success = await updateLeadStatus(lead.type, lead.id, newStatus);

        if (success) {
            toast.success(`Moved to ${newStatus}`);
        } else {
            // Revert
            leads = leads.map((l) =>
                l.id === lead.id ? { ...l, status: originalStatus } : l,
            );
        }
    }

    function handleDragStart(event: DragEvent, lead: Lead) {
        draggingLead = lead;
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = "move";
            event.dataTransfer.setData("text/plain", JSON.stringify(lead));
        }
    }

    function handleDragOver(event: DragEvent) {
        event.preventDefault();
        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = "move";
        }
    }

    function handleDrop(event: DragEvent, status: string) {
        event.preventDefault();
        if (draggingLead && draggingLead.status !== status) {
            handleStatusUpdate(draggingLead, status);
        }
        draggingLead = null;
    }
</script>

<div class="h-[calc(100vh-6rem)] flex flex-col">
    <div class="flex items-center justify-between mb-4 px-1">
        <h1 class="text-2xl font-bold">Lead Pipeline</h1>
        <div class="flex gap-2">
            <Button
                variant="outline"
                size="sm"
                onclick={handleExport}
                disabled={exporting}
            >
                {#if exporting}
                    <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                {:else}
                    <Download class="mr-2 h-4 w-4" />
                {/if}
                Export CSV
            </Button>
            <Button
                variant="outline"
                size="sm"
                onclick={loadLeads}
                disabled={loading}
            >
                {#if loading}
                    <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                {/if}
                Refresh
            </Button>
        </div>
    </div>

    <div class="flex-1 overflow-x-auto pb-2">
        <div class="flex gap-4 min-w-max h-full">
            {#each columns as col}
                <div
                    class="w-72 flex-shrink-0 bg-gray-50/50 rounded-lg flex flex-col border border-gray-200 max-h-full"
                    ondragover={handleDragOver}
                    ondrop={(e) => handleDrop(e, col.id)}
                    role="region"
                    aria-label="{col.label} column"
                >
                    <div
                        class="p-3 border-b border-border flex items-center justify-between bg-card/50 backdrop-blur-sm rounded-t-lg sticky top-0 z-10"
                    >
                        <span
                            class="font-semibold text-sm flex items-center gap-2"
                        >
                            <span
                                class={`w-2 h-2 rounded-full ${col.color.split(" ")[0].replace("bg-", "bg-")}`}
                            ></span>
                            {col.label}
                        </span>
                        <span
                            class="text-xs text-muted-foreground font-medium bg-card px-2 py-0.5 rounded-full border border-border shadow-sm"
                        >
                            {leads.filter((l) => l.status === col.id).length}
                        </span>
                    </div>

                    <div
                        class="p-2 flex-1 overflow-y-auto space-y-2 scrollbar-thin scrollbar-thumb-gray-200"
                    >
                        {#if loading}
                            {#each Array(3) as _}
                                <Skeleton class="h-24 w-full rounded-lg" />
                            {/each}
                        {:else}
                            {@const columnLeads = leads.filter(
                                (l) => l.status === col.id,
                            )}
                            {#if columnLeads.length === 0}
                                <div
                                    class="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50 min-h-[100px]"
                                >
                                    <p class="text-xs">No leads</p>
                                </div>
                            {:else}
                                {#each columnLeads as lead (lead.id)}
                                    <div
                                        draggable="true"
                                        ondragstart={(e) =>
                                            handleDragStart(e, lead)}
                                        class="bg-card p-3 rounded-lg shadow-sm border border-border cursor-move hover:shadow-md hover:border-primary/20 transition-all group"
                                        role="button"
                                        tabindex="0"
                                    >
                                        <div
                                            class="flex items-start justify-between mb-2"
                                        >
                                            <div class="flex gap-1 flex-wrap">
                                                <span
                                                    class={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider ${lead.type === "inquiry" ? "bg-blue-50 text-blue-600" : "bg-purple-50 text-purple-600"}`}
                                                >
                                                    {lead.type}
                                                </span>
                                                {#if lead.source}
                                                    <span
                                                        class="text-[10px] font-medium px-1.5 py-0.5 rounded bg-gray-50 text-gray-500 flex items-center gap-1 border border-gray-100"
                                                    >
                                                        {#if lead.source === "Website"}
                                                            <Globe size={10} />
                                                        {:else}
                                                            <User size={10} />
                                                        {/if}
                                                        {lead.source}
                                                    </span>
                                                {/if}
                                            </div>
                                            <span
                                                class="text-[10px] text-gray-400 whitespace-nowrap ml-2"
                                            >
                                                {new Date(
                                                    lead.createdAt,
                                                ).toLocaleDateString()}
                                            </span>
                                        </div>

                                        <h3
                                            class="font-medium text-sm text-gray-900 mb-1 line-clamp-1 group-hover:text-primary transition-colors"
                                        >
                                            {lead.name || "Unknown User"}
                                        </h3>
                                        <p
                                            class="text-xs text-gray-500 mb-3 line-clamp-2"
                                        >
                                            {lead.title}
                                        </p>

                                        <div
                                            class="flex items-center justify-between pt-2 border-t border-gray-50"
                                        >
                                            <div class="flex gap-1">
                                                {#if lead.email}
                                                    <a
                                                        href="mailto:{lead.email}"
                                                        class="p-1 text-gray-400 hover:text-primary hover:bg-gray-50 rounded transition-colors"
                                                        title="Email"
                                                        class:pointer-events-none={!lead.email}
                                                    >
                                                        <Mail size={14} />
                                                    </a>
                                                {/if}
                                            </div>
                                            <a
                                                href="/admin/leads/{lead.type}/{lead.id}"
                                                class="text-xs font-medium text-primary hover:underline opacity-0 group-hover:opacity-100 transition-opacity"
                                            >
                                                View
                                            </a>
                                        </div>
                                    </div>
                                {/each}
                            {/if}
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>
