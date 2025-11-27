<script lang="ts">
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    import { toast } from "svelte-sonner";
    import { ArrowLeft, Mail, Phone, FileText, Send } from "lucide-svelte";
    import {
        fetchLeadDetails,
        updateLeadStatus,
        addLeadNote,
        type Lead,
    } from "$lib/services/leads";

    const type = $page.params.type as string;
    const id = $page.params.id as string;

    let lead: Lead | null = null;
    let loading = true;
    let newNote = "";
    let submittingNote = false;

    const statuses = ["new", "contacted", "qualified", "converted", "lost"];

    onMount(async () => {
        await loadLead();
    });

    async function loadLead() {
        loading = true;
        lead = await fetchLeadDetails(type, id);
        loading = false;
    }

    async function handleStatusChange(newStatus: string) {
        if (!lead) return;
        const success = await updateLeadStatus(type, id, newStatus);
        if (success) {
            lead.status = newStatus;
            toast.success("Status updated");
        }
    }

    async function handleAddNote() {
        if (!newNote.trim() || !lead) return;

        submittingNote = true;
        const note = await addLeadNote(type, id, newNote);

        if (note) {
            lead.notes = [...(lead.notes || []), note];
            newNote = "";
            toast.success("Note added");
        }
        submittingNote = false;
    }
</script>

<div class="max-w-4xl mx-auto">
    <Button
        variant="ghost"
        href="/admin/leads"
        class="mb-4 pl-0 hover:pl-2 transition-all"
    >
        <ArrowLeft class="mr-2 h-4 w-4" /> Back to Leads
    </Button>

    {#if loading}
        <div class="p-8 text-center text-gray-500">Loading...</div>
    {:else if lead}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Main Content -->
            <div class="md:col-span-2 space-y-6">
                <!-- Header Card -->
                <div
                    class="bg-card p-6 rounded-lg shadow-sm border border-border"
                >
                    <div class="flex items-start justify-between mb-4">
                        <div>
                            <div class="flex items-center gap-2 mb-1">
                                <span
                                    class={`text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider ${lead.type === "inquiry" ? "bg-blue-100 text-blue-700" : "bg-purple-100 text-purple-700"}`}
                                >
                                    {lead.type}
                                </span>
                                {#if lead.source}
                                    <span
                                        class="text-xs font-medium px-2 py-0.5 rounded bg-gray-100 text-gray-600"
                                    >
                                        {lead.source}
                                    </span>
                                {/if}
                                <span class="text-xs text-gray-500">
                                    ID: {lead.id.slice(0, 8)}
                                </span>
                            </div>
                            <h1 class="text-2xl font-bold text-gray-900">
                                {lead.name || "Unknown User"}
                            </h1>
                            <p class="text-gray-500">{lead.title}</p>
                        </div>
                        <div class="flex flex-col items-end gap-2">
                            <select
                                value={lead.status}
                                onchange={(e) =>
                                    handleStatusChange(e.currentTarget.value)}
                                class="text-sm border-gray-300 rounded-md shadow-sm focus:border-primary focus:ring focus:ring-primary/50 capitalize"
                            >
                                {#each statuses as status}
                                    <option value={status}>{status}</option>
                                {/each}
                            </select>
                            <span class="text-xs text-gray-400">
                                Created {new Date(
                                    lead.createdAt,
                                ).toLocaleDateString()}
                            </span>
                        </div>
                    </div>

                    <div
                        class="grid grid-cols-2 gap-4 mt-6 pt-6 border-t border-gray-100"
                    >
                        {#if lead.email}
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500"
                                >
                                    <Mail size={16} />
                                </div>
                                <div>
                                    <p class="text-xs text-gray-500">Email</p>
                                    <a
                                        href="mailto:{lead.email}"
                                        class="text-sm font-medium text-primary hover:underline"
                                        >{lead.email}</a
                                    >
                                </div>
                            </div>
                        {/if}
                        {#if lead.phone}
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500"
                                >
                                    <Phone size={16} />
                                </div>
                                <div>
                                    <p class="text-xs text-gray-500">Phone</p>
                                    <a
                                        href="tel:{lead.phone}"
                                        class="text-sm font-medium text-primary hover:underline"
                                        >{lead.phone}</a
                                    >
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>

                <!-- Content Card -->
                <div
                    class="bg-card p-6 rounded-lg shadow-sm border border-border"
                >
                    <h2 class="font-semibold mb-4 flex items-center gap-2">
                        <FileText size={18} />
                        Details
                    </h2>
                    {#if lead.type === "inquiry"}
                        <div
                            class="prose prose-sm max-w-none bg-gray-50 p-4 rounded-lg"
                        >
                            <p class="whitespace-pre-wrap">{lead.message}</p>
                        </div>
                        {#if lead.property_title}
                            <div class="mt-4 pt-4 border-t border-gray-100">
                                <p class="text-sm text-gray-600">
                                    Interested in property:
                                    <a
                                        href="/properties/{lead.property_id}"
                                        class="font-medium text-primary hover:underline"
                                        target="_blank"
                                    >
                                        {lead.property_title}
                                    </a>
                                </p>
                            </div>
                        {/if}
                    {:else}
                        <div class="bg-gray-50 p-4 rounded-lg space-y-2">
                            {#each Object.entries(lead.criteria || {}) as [key, value]}
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-500 capitalize"
                                        >{key
                                            .replace(/([A-Z])/g, " $1")
                                            .trim()}</span
                                    >
                                    <span class="font-medium">{value}</span>
                                </div>
                            {/each}
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Sidebar -->
            <div class="space-y-6">
                <!-- Notes -->
                <div
                    class="bg-card p-6 rounded-lg shadow-sm border border-border h-full flex flex-col"
                >
                    <h2 class="font-semibold mb-4">Internal Notes</h2>

                    <div
                        class="flex-1 overflow-y-auto max-h-[400px] space-y-4 mb-4 pr-2"
                    >
                        {#if lead.notes && lead.notes.length > 0}
                            {#each lead.notes as note}
                                <div
                                    class="bg-yellow-50 p-3 rounded-lg border border-yellow-100 text-sm"
                                >
                                    <p class="text-gray-800 mb-1">
                                        {note.text}
                                    </p>
                                    <div
                                        class="flex justify-between items-center text-xs text-gray-400"
                                    >
                                        <span>{note.author}</span>
                                        <span
                                            >{new Date(
                                                note.timestamp,
                                            ).toLocaleDateString()}</span
                                        >
                                    </div>
                                </div>
                            {/each}
                        {:else}
                            <p
                                class="text-sm text-gray-400 italic text-center py-4"
                            >
                                No notes yet
                            </p>
                        {/if}
                    </div>

                    <div class="mt-auto pt-4 border-t border-gray-100">
                        <textarea
                            bind:value={newNote}
                            placeholder="Add a note..."
                            class="w-full text-sm border-gray-300 rounded-md focus:border-primary focus:ring focus:ring-primary/50 mb-2 resize-none"
                            rows="3"
                        ></textarea>
                        <Button
                            size="sm"
                            class="w-full"
                            onclick={handleAddNote}
                            disabled={submittingNote || !newNote.trim()}
                        >
                            <Send class="mr-2 h-3 w-3" /> Add Note
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    {:else}
        <div class="p-8 text-center text-red-500">Lead not found</div>
    {/if}
</div>
