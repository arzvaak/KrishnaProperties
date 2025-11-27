<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { ChevronLeft, ChevronRight, ArrowLeft } from "lucide-svelte";
    import emblaCarouselSvelte from "embla-carousel-svelte";
    import Autoplay from "embla-carousel-autoplay";

    export let images: string[] = [];
    export let title: string;
    export let backLink = "/properties";

    let emblaApi: any;
    let selectedIndex = 0;

    function onInit(event: CustomEvent) {
        emblaApi = event.detail;
        emblaApi.on("select", () => {
            selectedIndex = emblaApi.selectedScrollSnap();
        });
    }
</script>

<div class="relative bg-black group">
    <div class="absolute top-4 left-4 z-20">
        <Button
            variant="secondary"
            size="sm"
            href={backLink}
            class="gap-2 backdrop-blur-md bg-white/80 hover:bg-white"
        >
            <ArrowLeft class="w-4 h-4" /> Back
        </Button>
    </div>

    <div
        class="overflow-hidden h-[60vh] lg:h-[70vh]"
        use:emblaCarouselSvelte={{
            options: { loop: true },
            plugins: [Autoplay({ delay: 6000 })],
        }}
        onemblaInit={onInit}
    >
        <div class="flex h-full">
            {#if images && images.length > 0}
                {#each images as image}
                    <div class="flex-[0_0_100%] min-w-0 relative h-full">
                        <img
                            src={image}
                            alt={title}
                            class="object-cover w-full h-full"
                            onerror={(e) => {
                                const img = e.currentTarget as HTMLImageElement;
                                img.onerror = null;
                                img.src =
                                    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80";
                            }}
                        />
                        <div
                            class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"
                        ></div>
                    </div>
                {/each}
            {:else}
                <div class="flex-[0_0_100%] min-w-0 relative h-full">
                    <img
                        src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
                        alt={title}
                        class="object-cover w-full h-full"
                    />
                </div>
            {/if}
        </div>
    </div>

    <!-- Carousel Controls -->
    <div
        class="absolute bottom-8 left-0 right-0 z-20 flex justify-center gap-2"
    >
        {#if images && images.length > 1}
            {#each images as _, i}
                <button
                    class="w-2 h-2 rounded-full transition-all {i ===
                    selectedIndex
                        ? 'bg-white w-6'
                        : 'bg-white/50 hover:bg-white/80'}"
                    onclick={() => emblaApi && emblaApi.scrollTo(i)}
                    aria-label="Go to slide {i + 1}"
                ></button>
            {/each}
        {/if}
    </div>

    <button
        class="absolute left-4 top-1/2 -translate-y-1/2 z-20 p-3 rounded-full bg-black/20 text-white backdrop-blur-md border border-white/10 hover:bg-black/40 transition-all opacity-0 group-hover:opacity-100"
        onclick={() => emblaApi && emblaApi.scrollPrev()}
        aria-label="Previous slide"
    >
        <ChevronLeft class="w-6 h-6" />
    </button>
    <button
        class="absolute right-4 top-1/2 -translate-y-1/2 z-20 p-3 rounded-full bg-black/20 text-white backdrop-blur-md border border-white/10 hover:bg-black/40 transition-all opacity-0 group-hover:opacity-100"
        onclick={() => emblaApi && emblaApi.scrollNext()}
        aria-label="Next slide"
    >
        <ChevronRight class="w-6 h-6" />
    </button>
</div>
