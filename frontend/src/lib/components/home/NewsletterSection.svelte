<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { toast } from "svelte-sonner";
    import { Loader2, Mail } from "lucide-svelte";
    import { reveal } from "$lib/actions/reveal";
    import { API_BASE_URL } from "$lib/config";

    let email = "";
    let loading = false;

    async function subscribe() {
        if (!email) {
            toast.error("Please enter your email address");
            return;
        }

        loading = true;
        try {
            const res = await fetch(
                `${API_BASE_URL}/api/newsletter/subscribe`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email }),
                },
            );

            const data = await res.json();

            if (res.ok) {
                toast.success(data.message);
                email = "";
            } else {
                toast.error(data.error || "Failed to subscribe");
            }
        } catch (e) {
            toast.error("An error occurred. Please try again.");
        } finally {
            loading = false;
        }
    }
</script>

<section
    class="py-24 bg-primary text-primary-foreground relative overflow-hidden"
>
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-10 pointer-events-none">
        <svg
            class="h-full w-full"
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
        >
            <path d="M0 100 C 20 0 50 0 100 100 Z" fill="currentColor" />
        </svg>
    </div>

    <div class="container px-4 relative z-10" use:reveal>
        <div class="max-w-3xl mx-auto text-center space-y-8">
            <div
                class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/10 backdrop-blur-sm mb-4"
            >
                <Mail class="w-8 h-8 text-amber-300" />
            </div>

            <h2 class="text-4xl md:text-5xl font-bold tracking-tight">
                Stay Ahead of the Market
            </h2>

            <p class="text-xl text-primary-foreground/80 leading-relaxed">
                Join our exclusive newsletter to receive the latest property
                listings, market insights, and investment opportunities directly
                in your inbox.
            </p>

            <div class="flex flex-col sm:flex-row gap-4 max-w-md mx-auto mt-8">
                <Input
                    type="email"
                    placeholder="Enter your email address"
                    class="h-12 bg-white/10 border-white/20 text-white placeholder:text-white/60 focus-visible:ring-amber-400"
                    bind:value={email}
                />
                <Button
                    size="lg"
                    variant="secondary"
                    class="h-12 px-8 font-semibold whitespace-nowrap"
                    onclick={subscribe}
                    disabled={loading}
                >
                    {#if loading}
                        <Loader2 class="mr-2 h-4 w-4 animate-spin" /> Subscribing...
                    {:else}
                        Subscribe Now
                    {/if}
                </Button>
            </div>

            <p class="text-sm text-primary-foreground/60 mt-4">
                We respect your privacy. Unsubscribe at any time.
            </p>
        </div>
    </div>
</section>
