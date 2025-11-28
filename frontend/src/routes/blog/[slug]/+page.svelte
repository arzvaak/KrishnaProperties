<script lang="ts">
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import {
        Calendar,
        User,
        ArrowLeft,
        Share2,
        Clock,
        Eye,
    } from "lucide-svelte";
    import { format } from "date-fns";
    import { toast } from "svelte-sonner";
    import { API_BASE_URL } from "$lib/config";
    import { marked } from "marked";
    import DOMPurify from "dompurify";
    import { settings } from "$lib/stores/settings";

    let blog: any = null;
    let relatedBlogs: any[] = [];
    let loading = true;
    let slug = $page.params.slug;

    $: slug = $page.params.slug;
    $: if (slug) {
        fetchBlog(slug);
    }

    async function fetchBlog(currentSlug: string) {
        loading = true;
        try {
            const res = await fetch(`${API_BASE_URL}/api/blogs/${currentSlug}`);
            if (res.ok) {
                blog = await res.json();
                fetchRelatedBlogs(blog.category, blog.id);
            } else {
                toast.error("Blog not found");
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    async function fetchRelatedBlogs(category: string, currentId: string) {
        try {
            const res = await fetch(
                `${API_BASE_URL}/api/blogs?category=${category}&limit=3`,
            );
            if (res.ok) {
                const all = await res.json();
                relatedBlogs = all
                    .filter((b: any) => b.id !== currentId)
                    .slice(0, 3);
            }
        } catch (e) {
            console.error(e);
        }
    }

    function shareBlog() {
        if (navigator.share) {
            navigator.share({
                title: blog.title,
                text: blog.excerpt,
                url: window.location.href,
            });
        } else {
            navigator.clipboard.writeText(window.location.href);
            toast.success("Link copied to clipboard");
        }
    }
</script>

<svelte:head>
    {#if blog}
        <title
            >{blog.meta_title || blog.title} | {$settings.general
                .siteName}</title
        >
        <meta
            name="description"
            content={blog.meta_description || blog.excerpt}
        />
        <meta
            name="keywords"
            content={blog.meta_keywords || $settings.seo.defaultKeywords}
        />

        <!-- Open Graph -->
        <meta property="og:title" content={blog.meta_title || blog.title} />
        <meta
            property="og:description"
            content={blog.meta_description || blog.excerpt}
        />
        <meta property="og:image" content={blog.image} />
        <meta property="og:type" content="article" />

        <!-- Twitter -->
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={blog.meta_title || blog.title} />
        <meta
            name="twitter:description"
            content={blog.meta_description || blog.excerpt}
        />
        <meta name="twitter:image" content={blog.image} />
    {/if}
</svelte:head>

<div class="min-h-screen bg-background pb-12">
    {#if loading}
        <div class="flex justify-center py-20">
            <div
                class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
            ></div>
        </div>
    {:else if blog}
        <!-- Header -->
        <div class="relative h-[400px] md:h-[500px] w-full overflow-hidden">
            <div class="absolute inset-0 bg-black/50 z-10"></div>
            <img
                src={blog.image || "/placeholder-blog.jpg"}
                alt={blog.title}
                class="w-full h-full object-cover"
            />
            <div
                class="absolute inset-0 z-20 container px-4 md:px-6 flex flex-col justify-end pb-12 md:pb-20"
            >
                <div class="max-w-4xl mx-auto w-full space-y-4">
                    <Button
                        variant="outline"
                        size="sm"
                        href="/blog"
                        class="text-white border-white/20 hover:bg-white/10 hover:text-white mb-4"
                    >
                        <ArrowLeft class="mr-2 h-4 w-4" /> Back to Articles
                    </Button>
                    <div class="flex items-center gap-3 text-white/80 text-sm">
                        <Badge
                            variant="secondary"
                            class="bg-primary text-primary-foreground hover:bg-primary/90"
                            >{blog.category || "General"}</Badge
                        >
                        <span class="flex items-center gap-1">
                            <Calendar class="h-4 w-4" />
                            {blog.created_at
                                ? format(
                                      new Date(blog.created_at),
                                      "MMMM d, yyyy",
                                  )
                                : ""}
                        </span>
                        <span class="flex items-center gap-1">
                            <Eye class="h-4 w-4" />
                            {blog.views || 0} views
                        </span>
                    </div>
                    <h1
                        class="text-3xl md:text-5xl lg:text-6xl font-bold text-white tracking-tight"
                    >
                        {blog.title}
                    </h1>
                </div>
            </div>
        </div>

        <div class="container px-4 md:px-6 py-12">
            <div class="grid lg:grid-cols-[1fr_300px] gap-12 max-w-6xl mx-auto">
                <!-- Main Content -->
                <article class="prose prose-lg dark:prose-invert max-w-none">
                    <div
                        class="flex justify-between items-center mb-8 not-prose border-b pb-4"
                    >
                        <div class="flex items-center gap-3">
                            <div
                                class="h-10 w-10 rounded-full bg-muted flex items-center justify-center"
                            >
                                <User class="h-5 w-5 text-muted-foreground" />
                            </div>
                            <div>
                                <p class="font-medium text-sm">Written by</p>
                                <p class="text-sm text-muted-foreground">
                                    Krishna Properties Team
                                </p>
                            </div>
                        </div>
                        <Button variant="ghost" size="sm" onclick={shareBlog}>
                            <Share2 class="mr-2 h-4 w-4" /> Share
                        </Button>
                    </div>

                    <!-- Content Render -->
                    <div class="blog-content">
                        {@html DOMPurify.sanitize(marked(blog.content))}
                    </div>

                    {#if blog.tags && blog.tags.length > 0}
                        <div class="mt-8 pt-8 border-t not-prose">
                            <h4 class="text-sm font-semibold mb-3">Tags</h4>
                            <div class="flex flex-wrap gap-2">
                                {#each blog.tags as tag}
                                    <Badge variant="outline">#{tag}</Badge>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </article>

                <!-- Sidebar -->
                <aside class="space-y-8">
                    {#if relatedBlogs.length > 0}
                        <div>
                            <h3 class="font-bold text-xl mb-4">
                                Related Articles
                            </h3>
                            <div class="space-y-4">
                                {#each relatedBlogs as related}
                                    <a
                                        href="/blog/{related.slug}"
                                        class="block group"
                                    >
                                        <div
                                            class="aspect-video rounded-lg overflow-hidden mb-2"
                                        >
                                            <img
                                                src={related.image ||
                                                    "/placeholder-blog.jpg"}
                                                alt={related.title}
                                                class="w-full h-full object-cover transition-transform group-hover:scale-105"
                                            />
                                        </div>
                                        <h4
                                            class="font-medium group-hover:text-primary transition-colors line-clamp-2"
                                        >
                                            {related.title}
                                        </h4>
                                        <p
                                            class="text-xs text-muted-foreground mt-1"
                                        >
                                            {related.created_at
                                                ? format(
                                                      new Date(
                                                          related.created_at,
                                                      ),
                                                      "MMM d, yyyy",
                                                  )
                                                : ""}
                                        </p>
                                    </a>
                                {/each}
                            </div>
                        </div>
                    {/if}

                    <Card>
                        <CardHeader>
                            <CardTitle>Newsletter</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p class="text-sm text-muted-foreground mb-4">
                                Subscribe to get the latest property news and
                                market updates.
                            </p>
                            <Button class="w-full">Subscribe</Button>
                        </CardContent>
                    </Card>
                </aside>
            </div>
        </div>
    {:else}
        <div class="container py-20 text-center">
            <h1 class="text-2xl font-bold">Blog not found</h1>
            <Button href="/blog" class="mt-4">Back to Blog</Button>
        </div>
    {/if}
</div>

<style>
    /* Add some basic typography styles for the blog content if tailwind typography plugin isn't enough or configured */
    .blog-content :global(h2) {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .blog-content :global(p) {
        margin-bottom: 1.5rem;
        line-height: 1.75;
    }
    .blog-content :global(ul) {
        list-style-type: disc;
        padding-left: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .blog-content :global(img) {
        border-radius: 0.5rem;
        margin: 2rem 0;
    }
</style>
