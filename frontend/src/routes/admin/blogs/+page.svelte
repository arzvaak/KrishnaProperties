<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    import * as Table from "$lib/components/ui/table";
    import * as Card from "$lib/components/ui/card";
    import { Badge } from "$lib/components/ui/badge";
    import { Input } from "$lib/components/ui/input";
    import { toast } from "svelte-sonner";
    import { Plus, Pencil, Trash2, Eye, Search, Loader2 } from "lucide-svelte";
    import { format } from "date-fns";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let blogs: any[] = [];
    let loading = true;
    let searchQuery = "";

    onMount(async () => {
        await fetchBlogs();
    });

    async function fetchBlogs() {
        loading = true;
        try {
            const res = await fetchWithAuth(`${API_BASE_URL}/api/admin/blogs`);
            if (res.ok) {
                blogs = await res.json();
            } else {
                toast.error("Failed to fetch blogs");
            }
        } catch (e) {
            toast.error("Error fetching blogs");
        } finally {
            loading = false;
        }
    }

    async function deleteBlog(id: string) {
        if (!confirm("Are you sure you want to delete this blog post?")) return;

        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/blogs/${id}`,
                {
                    method: "DELETE",
                },
            );

            if (res.ok) {
                toast.success("Blog deleted successfully");
                blogs = blogs.filter((b) => b.id !== id);
            } else {
                toast.error("Failed to delete blog");
            }
        } catch (e) {
            toast.error("Error deleting blog");
        }
    }

    $: filteredBlogs = blogs.filter((blog) =>
        blog.title.toLowerCase().includes(searchQuery.toLowerCase()),
    );
</script>

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">Blog Posts</h2>
            <p class="text-muted-foreground">
                Manage your articles and content.
            </p>
        </div>
        <Button href="/admin/blogs/editor">
            <Plus class="mr-2 h-4 w-4" /> Create New Post
        </Button>
    </div>

    <div class="flex items-center py-4">
        <div class="relative max-w-sm w-full">
            <Search
                class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground"
            />
            <Input
                placeholder="Search posts..."
                class="pl-8"
                bind:value={searchQuery}
            />
        </div>
    </div>

    {#if loading}
        <div class="flex justify-center py-8">
            <Loader2 class="h-8 w-8 animate-spin text-primary" />
        </div>
    {:else}
        <Card.Root>
            <Card.Content class="p-0">
                <Table.Root>
                    <Table.Header>
                        <Table.Row>
                            <Table.Head>Title</Table.Head>
                            <Table.Head>Category</Table.Head>
                            <Table.Head>Status</Table.Head>
                            <Table.Head>Views</Table.Head>
                            <Table.Head>Date</Table.Head>
                            <Table.Head class="text-right">Actions</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each filteredBlogs as blog}
                            <Table.Row>
                                <Table.Cell class="font-medium">
                                    <div class="flex items-center gap-2">
                                        {#if blog.image}
                                            <img
                                                src={blog.image}
                                                alt={blog.title}
                                                class="h-8 w-8 rounded object-cover"
                                            />
                                        {/if}
                                        <span class="truncate max-w-[300px]"
                                            >{blog.title}</span
                                        >
                                    </div>
                                </Table.Cell>
                                <Table.Cell
                                    >{blog.category ||
                                        "Uncategorized"}</Table.Cell
                                >
                                <Table.Cell>
                                    {#if blog.published}
                                        <Badge class="bg-green-500"
                                            >Published</Badge
                                        >
                                    {:else}
                                        <Badge variant="outline">Draft</Badge>
                                    {/if}
                                    {#if blog.featured}
                                        <Badge variant="secondary" class="ml-1"
                                            >Featured</Badge
                                        >
                                    {/if}
                                </Table.Cell>
                                <Table.Cell>{blog.views || 0}</Table.Cell>
                                <Table.Cell>
                                    {blog.created_at
                                        ? format(
                                              new Date(blog.created_at),
                                              "MMM d, yyyy",
                                          )
                                        : "-"}
                                </Table.Cell>
                                <Table.Cell class="text-right">
                                    <div class="flex justify-end gap-2">
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            href="/blog/{blog.slug}"
                                            target="_blank"
                                            title="View"
                                        >
                                            <Eye class="h-4 w-4" />
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            href="/admin/blogs/editor?id={blog.id}"
                                            title="Edit"
                                        >
                                            <Pencil class="h-4 w-4" />
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            class="text-red-500 hover:text-red-600"
                                            onclick={() => deleteBlog(blog.id)}
                                            title="Delete"
                                        >
                                            <Trash2 class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </Table.Cell>
                            </Table.Row>
                        {/each}
                        {#if filteredBlogs.length === 0}
                            <Table.Row>
                                <Table.Cell
                                    colspan={6}
                                    class="text-center py-8 text-muted-foreground"
                                >
                                    No blog posts found.
                                </Table.Cell>
                            </Table.Row>
                        {/if}
                    </Table.Body>
                </Table.Root>
            </Card.Content>
        </Card.Root>
    {/if}
</div>
