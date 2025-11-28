<script lang="ts">
    import { reveal } from "$lib/actions/reveal";
    import { Card, CardContent } from "$lib/components/ui/card";
    import { Users, Award, Building, History } from "lucide-svelte";
</script>

<div class="container py-12 pt-24">
    <div class="max-w-3xl mx-auto text-center mb-16" use:reveal>
        <h1 class="text-4xl md:text-5xl font-bold mb-6">
            About Krishna Properties
        </h1>
        <p class="text-xl text-muted-foreground leading-relaxed">
            We are more than just a real estate agency. We are your partners in
            finding the perfect place to call home.
        </p>
    </div>

    <div class="grid md:grid-cols-2 gap-12 items-center mb-24">
        <div use:reveal={{ delay: 100 }}>
            <img
                src="/images/hero-bg-v2.png"
                alt="Our Office"
                class="rounded-2xl shadow-2xl object-cover h-[400px] w-full"
            />
        </div>
        <div class="space-y-6" use:reveal={{ delay: 200 }}>
            <h2 class="text-3xl font-bold">Our Story</h2>
            <p class="text-muted-foreground leading-relaxed">
                Founded in 2010, Krishna Properties began with a simple mission:
                to bring transparency, trust, and excellence to the real estate
                market in Mumbai. Over the years, we have grown from a small
                boutique agency to a premier real estate firm, serving thousands
                of happy clients.
            </p>
            <p class="text-muted-foreground leading-relaxed">
                Our deep understanding of the local market, combined with our
                commitment to personalized service, sets us apart. We believe
                that every client deserves a seamless and enjoyable real estate
                journey.
            </p>
        </div>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-24">
        <div
            class="text-center p-6 bg-muted/30 rounded-xl"
            use:reveal={{ delay: 100 }}
        >
            <History class="w-10 h-10 mx-auto text-primary mb-4" />
            <div class="text-3xl font-bold mb-1">15+</div>
            <div class="text-sm text-muted-foreground">Years Experience</div>
        </div>
        <div
            class="text-center p-6 bg-muted/30 rounded-xl"
            use:reveal={{ delay: 200 }}
        >
            <Building class="w-10 h-10 mx-auto text-primary mb-4" />
            <div class="text-3xl font-bold mb-1">500+</div>
            <div class="text-sm text-muted-foreground">Properties Sold</div>
        </div>
        <div
            class="text-center p-6 bg-muted/30 rounded-xl"
            use:reveal={{ delay: 300 }}
        >
            <Users class="w-10 h-10 mx-auto text-primary mb-4" />
            <div class="text-3xl font-bold mb-1">2000+</div>
            <div class="text-sm text-muted-foreground">Happy Clients</div>
        </div>
        <div
            class="text-center p-6 bg-muted/30 rounded-xl"
            use:reveal={{ delay: 400 }}
        >
            <Award class="w-10 h-10 mx-auto text-primary mb-4" />
            <div class="text-3xl font-bold mb-1">10+</div>
            <div class="text-sm text-muted-foreground">Industry Awards</div>
        </div>
    </div>

    <div class="mb-12">
        <h2 class="text-3xl font-bold text-center mb-12">
            Meet Our Leadership
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
            {#each [1, 2, 3] as i}
                <div use:reveal={{ delay: i * 100 }}>
                    <Card class="overflow-hidden group">
                        <div class="h-64 overflow-hidden">
                            <img
                                src={`https://api.dicebear.com/7.x/avataaars/svg?seed=Team${i}`}
                                alt="Team Member"
                                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                            />
                        </div>
                        <CardContent class="p-6 text-center">
                            <h3 class="font-bold text-xl mb-1">
                                {["Rajesh Kumar", "Priya Sharma", "Amit Patel"][
                                    i - 1
                                ]}
                            </h3>
                            <p class="text-primary font-medium mb-4">
                                {[
                                    "Founder & CEO",
                                    "Head of Sales",
                                    "Senior Consultant",
                                ][i - 1]}
                            </p>
                            <p class="text-sm text-muted-foreground">
                                Dedicated to delivering excellence and ensuring
                                client satisfaction at every step.
                            </p>
                        </CardContent>
                    </Card>
                </div>
            {/each}
        </div>
    </div>
</div>
