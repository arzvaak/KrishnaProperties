<script lang="ts">
    import { Home, TrendingUp, Users, ShieldCheck } from "lucide-svelte";
    import { reveal } from "$lib/actions/reveal";
</script>

<section class="py-32 bg-muted/30 relative overflow-hidden">
    <!-- Decorative background element -->
    <div
        class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-5"
    >
        <div
            class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-primary blur-3xl"
        ></div>
        <div
            class="absolute -bottom-[20%] -right-[10%] w-[50%] h-[50%] rounded-full bg-amber-500 blur-3xl"
        ></div>
    </div>

    <div class="container px-4 relative z-10">
        <div class="text-center max-w-3xl mx-auto mb-20" use:reveal>
            <h2 class="text-4xl font-bold mb-6">
                Why Choose Krishna Properties
            </h2>
            <p class="text-xl text-muted-foreground">
                Excellence in every detail of your real estate journey.
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div
                class="text-center group p-6 rounded-2xl hover:bg-background/50 transition-colors duration-300"
                use:reveal={{ threshold: 0.1 }}
            >
                <div
                    class="w-20 h-20 mx-auto bg-background rounded-full flex items-center justify-center shadow-lg mb-8 group-hover:scale-110 group-hover:shadow-primary/20 transition-all duration-300"
                >
                    <Home
                        class="w-8 h-8 text-primary group-hover:text-amber-500 transition-colors"
                    />
                </div>
                <h3 class="text-2xl font-bold mb-4">Premium Portfolio</h3>
                <p class="text-muted-foreground leading-relaxed">
                    Access to the most exclusive and high-end properties in the
                    market, curated for quality and luxury.
                </p>
            </div>
            <div
                class="text-center group p-6 rounded-2xl hover:bg-background/50 transition-colors duration-300"
                use:reveal={{ threshold: 0.1, delay: 100 }}
            >
                <div
                    class="w-20 h-20 mx-auto bg-background rounded-full flex items-center justify-center shadow-lg mb-8 group-hover:scale-110 group-hover:shadow-primary/20 transition-all duration-300"
                >
                    <TrendingUp
                        class="w-8 h-8 text-primary group-hover:text-amber-500 transition-colors"
                    />
                </div>
                <h3 class="text-2xl font-bold mb-4">Market Insight</h3>
                <p class="text-muted-foreground leading-relaxed">
                    Deep data-driven analysis to ensure you make the best
                    investment decisions in a fluctuating market.
                </p>
            </div>
            <div
                class="text-center group p-6 rounded-2xl hover:bg-background/50 transition-colors duration-300"
                use:reveal={{ threshold: 0.1, delay: 200 }}
            >
                <div
                    class="w-20 h-20 mx-auto bg-background rounded-full flex items-center justify-center shadow-lg mb-8 group-hover:scale-110 group-hover:shadow-primary/20 transition-all duration-300"
                >
                    <Users
                        class="w-8 h-8 text-primary group-hover:text-amber-500 transition-colors"
                    />
                </div>
                <h3 class="text-2xl font-bold mb-4">Personalized Care</h3>
                <p class="text-muted-foreground leading-relaxed">
                    We treat every client's search as if it were our own,
                    providing dedicated support at every step.
                </p>
            </div>
        </div>
    </div>
</section>
