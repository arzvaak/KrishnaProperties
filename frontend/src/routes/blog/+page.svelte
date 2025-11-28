<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Badge } from "$lib/components/ui/badge";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
        CardDescription,
        CardFooter,
    } from "$lib/components/ui/card";
    import { Search, Calendar, User, ArrowRight, Loader2 } from "lucide-svelte";
    import { format } from "date-fns";
    import { API_BASE_URL } from "$lib/config";

    let blogs: any[] = [];
    let categories: any[] = [];
    let loading = true;
    let selectedCategory = "";
    let searchQuery = "";

    onMount(async () => {
        await Promise.all([fetchBlogs(), fetchCategories()]);
    });

    async function fetchBlogs() {
        loading = true;
        try {
            let url = `${API_BASE_URL}/api/blogs`;
            if (selectedCategory) {
                url += `?category=${selectedCategory}`;
            }
            const res = await fetch(url);
            if (res.ok) {
                blogs = await res.json();
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    async function fetchCategories() {
        try {
            const res = await fetch(`${API_BASE_URL}/api/blog-categories`);
            if (res.ok) {
                categories = await res.json();
            }
        } catch (e) {
            console.error(e);
        }
    }

    function handleCategoryClick(cat: string) {
        selectedCategory = selectedCategory === cat ? "" : cat;
        fetchBlogs();
    }

    $: filteredBlogs = blogs.filter(
        (blog) =>
            blog.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            blog.excerpt?.toLowerCase().includes(searchQuery.toLowerCase()),
    );

    $: featuredBlog = filteredBlogs.find((b) => b.featured) || filteredBlogs[0];
    $: recentBlogs = filteredBlogs.filter((b) => b.id !== featuredBlog?.id);
</script>

<div class="min-h-screen bg-background pb-12">
    <!-- Hero Section -->
    <section class="relative bg-muted/40 py-12 md:py-20">
        <div class="container px-4 md:px-6">
            <div class="mx-auto max-w-3xl text-center">
                <h1
                    class="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl"
                >
                    Real Estate Insights
                </h1>
                <p class="mt-4 text-lg text-muted-foreground md:text-xl">
                    Expert advice, market trends, and tips for buyers and
                    sellers.
                </p>

                <div class="mt-8 flex justify-center">
                    <div class="relative w-full max-w-md">
                        <Search
                            class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
                        />
                        <Input
                            type="search"
                            placeholder="Search articles..."
                            class="pl-10 h-10 bg-background"
                            bind:value={searchQuery}
                        />
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="container px-4 md:px-6 mt-12">
        {#if loading}
            <div class="flex justify-center py-12">
                <Loader2 class="h-8 w-8 animate-spin text-primary" />
            </div>
        {:else if filteredBlogs.length === 0}
            <div class="text-center py-12 text-muted-foreground">
                No articles found matching your criteria.
            </div>
        {:else}
            <!-- Featured Post -->
            {#if featuredBlog && !searchQuery && !selectedCategory}
                <div class="mb-12">
                    <h2 class="text-2xl font-bold mb-6">Featured Article</h2>
                    <div
                        class="grid md:grid-cols-2 gap-8 items-center rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden"
                    >
                        <div
                            class="aspect-video md:aspect-auto md:h-full relative overflow-hidden"
                        >
                            <img
                                src={featuredBlog.image ||
                                    "/placeholder-blog.jpg"}
                                alt={featuredBlog.title}
                                class="object-cover w-full h-full transition-transform hover:scale-105 duration-500"
                            />
                        </div>
                        <div class="p-6 md:p-8 space-y-4">
                            <div
                                class="flex items-center gap-2 text-sm text-muted-foreground"
                            >
                                <Badge variant="secondary"
                                    >{featuredBlog.category || "General"}</Badge
                                >
                                <span>•</span>
                                <span
                                    >{featuredBlog.created_at
                                        ? format(
                                              new Date(featuredBlog.created_at),
                                              "MMM d, yyyy",
                                          )
                                        : "Recent"}</span
                                >
                            </div>
                            <h3
                                class="text-3xl font-bold tracking-tight hover:text-primary transition-colors"
                            >
                                <a href="/blog/{featuredBlog.slug}"
                                    >{featuredBlog.title}</a
                                >
                            </h3>
                            <p class="text-muted-foreground line-clamp-3">
                                {featuredBlog.excerpt}
                            </p>
                            <Button
                                variant="link"
                                class="px-0 text-primary"
                                href="/blog/{featuredBlog.slug}"
                            >
                                Read Article <ArrowRight class="ml-2 h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                </div>
            {/if}

            <!-- Recent Posts Grid -->
            <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {#each searchQuery || selectedCategory ? filteredBlogs : recentBlogs as blog}
                    <Card
                        class="flex flex-col h-full overflow-hidden hover:shadow-lg transition-shadow"
                    >
                        <div class="aspect-video relative overflow-hidden">
                            <img
                                src={blog.image || "/placeholder-blog.jpg"}
                                alt={blog.title}
                                class="object-cover w-full h-full transition-transform hover:scale-105 duration-500"
                            />
                        </div>
                        <CardHeader>
                            <div
                                class="flex items-center justify-between text-sm text-muted-foreground mb-2"
                            >
                                <Badge variant="outline"
                                    >{blog.category || "General"}</Badge
                                >
                                <span class="flex items-center gap-1">
                                    <Calendar class="h-3 w-3" />
                                    {blog.created_at
                                        ? format(
                                              new Date(blog.created_at),
                                              "MMM d",
                                          )
                                        : ""}
                                </span>
                            </div>
                            <CardTitle
                                class="line-clamp-2 hover:text-primary transition-colors"
                            >
                                <a href="/blog/{blog.slug}">{blog.title}</a>
                            </CardTitle>
                        </CardHeader>
                        <CardContent class="flex-1">
                            <p
                                class="text-muted-foreground line-clamp-3 text-sm"
                            >
                                {blog.excerpt}
                            </p>
                        </CardContent>
                        <CardFooter>
                            <Button
                                variant="ghost"
                                class="w-full justify-between"
                                href="/blog/{blog.slug}"
                            >
                                Read More <ArrowRight class="h-4 w-4" />
                            </Button>
                        </CardFooter>
                    </Card>
                {/each}
            </div>
        {/if}
    </div>
</div>
