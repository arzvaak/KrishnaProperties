<script lang="ts">
    import { reveal } from "$lib/actions/reveal";
    import { Search, Home, FileCheck, Key } from "lucide-svelte";
</script>

<div class="container py-12 pt-24">
    <div class="text-center max-w-3xl mx-auto mb-16" use:reveal>
        <h1 class="text-4xl font-bold mb-6">How It Works</h1>
        <p class="text-xl text-muted-foreground">
            Your journey to finding the perfect home, simplified.
        </p>
    </div>

    <div class="relative max-w-4xl mx-auto">
        <!-- Connecting Line -->
        <div
            class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-border -translate-x-1/2 hidden md:block"
        ></div>

        <div class="space-y-12 md:space-y-24">
            <!-- Step 1 -->
            <div
                class="relative flex flex-col md:flex-row items-center gap-8 md:gap-16"
                use:reveal={{ delay: 100 }}
            >
                <div class="md:w-1/2 text-right order-2 md:order-1">
                    <h3 class="text-2xl font-bold mb-2">
                        1. Search & Discover
                    </h3>
                    <p class="text-muted-foreground">
                        Browse our curated list of premium properties. Use our
                        advanced filters to narrow down your options by
                        location, price, and amenities.
                    </p>
                </div>
                <div
                    class="relative z-10 flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground shadow-xl order-1 md:order-2"
                >
                    <Search class="w-8 h-8" />
                </div>
                <div class="md:w-1/2 order-3"></div>
            </div>

            <!-- Step 2 -->
            <div
                class="relative flex flex-col md:flex-row items-center gap-8 md:gap-16"
                use:reveal={{ delay: 200 }}
            >
                <div class="md:w-1/2 order-2 md:order-1"></div>
                <div
                    class="relative z-10 flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground shadow-xl order-1 md:order-2"
                >
                    <Home class="w-8 h-8" />
                </div>
                <div class="md:w-1/2 text-left order-3">
                    <h3 class="text-2xl font-bold mb-2">2. Schedule a Visit</h3>
                    <p class="text-muted-foreground">
                        Found something you like? Schedule a private viewing at
                        your convenience. Our agents will give you a detailed
                        tour and answer all your questions.
                    </p>
                </div>
            </div>

            <!-- Step 3 -->
            <div
                class="relative flex flex-col md:flex-row items-center gap-8 md:gap-16"
                use:reveal={{ delay: 300 }}
            >
                <div class="md:w-1/2 text-right order-2 md:order-1">
                    <h3 class="text-2xl font-bold mb-2">3. Make an Offer</h3>
                    <p class="text-muted-foreground">
                        Once you've found "the one," we'll help you draft a
                        competitive offer and negotiate the best price and terms
                        with the seller.
                    </p>
                </div>
                <div
                    class="relative z-10 flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground shadow-xl order-1 md:order-2"
                >
                    <FileCheck class="w-8 h-8" />
                </div>
                <div class="md:w-1/2 order-3"></div>
            </div>

            <!-- Step 4 -->
            <div
                class="relative flex flex-col md:flex-row items-center gap-8 md:gap-16"
                use:reveal={{ delay: 400 }}
            >
                <div class="md:w-1/2 order-2 md:order-1"></div>
                <div
                    class="relative z-10 flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground shadow-xl order-1 md:order-2"
                >
                    <Key class="w-8 h-8" />
                </div>
                <div class="md:w-1/2 text-left order-3">
                    <h3 class="text-2xl font-bold mb-2">4. Close & Move In</h3>
                    <p class="text-muted-foreground">
                        We'll guide you through the closing process, paperwork,
                        and handover. Congratulations, the keys to your new home
                        are yours!
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
