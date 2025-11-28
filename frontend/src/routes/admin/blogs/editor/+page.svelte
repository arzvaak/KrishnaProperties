<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";
    import { Switch } from "$lib/components/ui/switch";
    import * as Select from "$lib/components/ui/select";
    import { toast } from "svelte-sonner";
    import {
        Loader2,
        Save,
        ArrowLeft,
        Image as ImageIcon,
    } from "lucide-svelte";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";
    import MarkdownEditor from "$lib/components/admin/MarkdownEditor.svelte";

    let loading = false;
    let saving = false;
    let isEditMode = false;
    let blogId: string | null = null;

    let formData = {
        title: "",
        content: "",
        excerpt: "",
        image: "",
        category: "",
        published: false,
        featured: false,
    };

    let categories: any[] = [];

    onMount(async () => {
        await fetchCategories();
        blogId = $page.url.searchParams.get("id");
        if (blogId) {
            isEditMode = true;
            await fetchBlog(blogId);
        }
    });

    async function fetchCategories() {
        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/blog-categories`,
            );
            if (res.ok) {
                categories = await res.json();
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchBlog(id: string) {
        loading = true;
        try {
            const res = await fetchWithAuth(`${API_BASE_URL}/api/admin/blogs`);
            if (res.ok) {
                const all = await res.json();
                const blog = all.find((b: any) => b.id === id);
                if (blog) {
                    formData = {
                        title: blog.title,
                        content: blog.content,
                        excerpt: blog.excerpt || "",
                        image: blog.image || "",
                        category: blog.category || "",
                        published: blog.published || false,
                        featured: blog.featured || false,
                    };
                } else {
                    toast.error("Blog not found");
                    goto("/admin/blogs");
                }
            }
        } catch (e) {
            toast.error("Error fetching blog details");
        } finally {
            loading = false;
        }
    }

    async function handleSubmit() {
        if (!formData.title || !formData.content) {
            toast.error("Title and Content are required");
            return;
        }

        saving = true;
        try {
            const url = isEditMode
                ? `${API_BASE_URL}/api/admin/blogs/${blogId}`
                : `${API_BASE_URL}/api/admin/blogs`;

            const method = isEditMode ? "PUT" : "POST";

            const res = await fetchWithAuth(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (res.ok) {
                toast.success(
                    isEditMode
                        ? "Blog updated successfully"
                        : "Blog created successfully",
                );
                goto("/admin/blogs");
            } else {
                const err = await res.json();
                toast.error(err.error || "Failed to save blog");
            }
        } catch (e) {
            toast.error("Error saving blog");
        } finally {
            saving = false;
        }
    }

    async function addCategory() {
        const name = prompt("Enter new category name:");
        if (!name) return;

        try {
            const res = await fetchWithAuth(
                `${API_BASE_URL}/api/admin/blog-categories`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name }),
                },
            );

            if (res.ok) {
                toast.success("Category added");
                fetchCategories();
            } else {
                toast.error("Failed to add category");
            }
        } catch (e) {
            toast.error("Error adding category");
        }
    }
</script>

<div class="max-w-4xl mx-auto space-y-8 pb-12">
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <Button variant="ghost" size="icon" href="/admin/blogs">
                <ArrowLeft class="h-4 w-4" />
            </Button>
            <div>
                <h2 class="text-3xl font-bold tracking-tight">
                    {isEditMode ? "Edit Post" : "New Post"}
                </h2>
                <p class="text-muted-foreground">
                    Write and manage your article.
                </p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <Button onclick={handleSubmit} disabled={saving}>
                {#if saving}
                    <Loader2 class="mr-2 h-4 w-4 animate-spin" /> Saving...
                {:else}
                    <Save class="mr-2 h-4 w-4" /> Save Post
                {/if}
            </Button>
        </div>
    </div>

    {#if loading}
        <div class="flex justify-center py-12">
            <Loader2 class="h-8 w-8 animate-spin text-primary" />
        </div>
    {:else}
        <div class="grid gap-8">
            <div class="grid gap-4">
                <div class="space-y-2">
                    <Label for="title">Title</Label>
                    <Input
                        id="title"
                        bind:value={formData.title}
                        placeholder="Enter post title"
                        class="text-lg font-medium"
                    />
                </div>

                <div class="grid md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <div class="flex justify-between items-center">
                            <Label>Category</Label>
                            <Button
                                variant="link"
                                size="sm"
                                class="h-auto p-0"
                                onclick={addCategory}>+ Add New</Button
                            >
                        </div>
                        <select
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                            bind:value={formData.category}
                        >
                            <option value="">Select Category</option>
                            {#each categories as cat}
                                <option value={cat.name}>{cat.name}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="space-y-2">
                        <Label for="image">Cover Image URL</Label>
                        <div class="flex gap-2">
                            <Input
                                id="image"
                                bind:value={formData.image}
                                placeholder="https://..."
                            />
                            {#if formData.image}
                                <Button
                                    variant="outline"
                                    size="icon"
                                    href={formData.image}
                                    target="_blank"
                                >
                                    <ImageIcon class="h-4 w-4" />
                                </Button>
                            {/if}
                        </div>
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="excerpt">Excerpt</Label>
                    <Textarea
                        id="excerpt"
                        bind:value={formData.excerpt}
                        placeholder="Short summary for listing cards..."
                        rows={3}
                    />
                </div>

                <div
                    class="grid md:grid-cols-2 gap-6 p-4 border rounded-lg bg-muted/20"
                >
                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Published</Label>
                            <p class="text-sm text-muted-foreground">
                                Visible to the public
                            </p>
                        </div>
                        <Switch bind:checked={formData.published} />
                    </div>
                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Featured</Label>
                            <p class="text-sm text-muted-foreground">
                                Show in hero section
                            </p>
                        </div>
                        <Switch bind:checked={formData.featured} />
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="content">Content (HTML/Markdown)</Label>
                    <p class="text-xs text-muted-foreground mb-2">
                        Supports basic HTML tags. Use <code>&lt;h2&gt;</code>,
                        <code>&lt;p&gt;</code>, <code>&lt;ul&gt;</code>, etc.
                    </p>
                    <MarkdownEditor bind:value={formData.content} />
                </div>
            </div>
        </div>
    {/if}
</div>
