<script lang="ts">
    import { Card, CardContent } from "$lib/components/ui/card";
    import { Quote } from "lucide-svelte";
    import { reveal } from "$lib/actions/reveal";

    const testimonials = [
        {
            name: "Sarah Johnson",
            role: "Luxury Villa Buyer",
            quote: "The level of service and attention to detail was outstanding. They truly understood what we were looking for.",
            seed: "Client1",
        },
        {
            name: "Michael Chen",
            role: "Property Investor",
            quote: "Krishna Properties helped me find high-yield investment opportunities that I wouldn't have found elsewhere.",
            seed: "Client2",
        },
        {
            name: "Emily Davis",
            role: "First-time Buyer",
            quote: "Guided me through every step of the process with patience and expertise. Highly recommended!",
            seed: "Client3",
        },
    ];
</script>

<section class="py-32 container px-4">
    <div class="text-center mb-20" use:reveal>
        <h2 class="text-4xl font-bold mb-4">Client Stories</h2>
        <p class="text-xl text-muted-foreground">
            Hear from those who found their dream home with us.
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {#each testimonials as client, i}
            <div use:reveal={{ delay: i * 100 }}>
                <Card
                    class="bg-muted/30 border-none hover:bg-muted/50 transition-colors duration-300"
                >
                    <CardContent class="p-8">
                        <Quote class="w-10 h-10 text-primary/20 mb-6" />
                        <p
                            class="text-lg text-muted-foreground mb-8 italic leading-relaxed"
                        >
                            "{client.quote}"
                        </p>
                        <div class="flex items-center gap-4">
                            <div
                                class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden ring-2 ring-primary/10"
                            >
                                <img
                                    src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${client.seed}`}
                                    alt={client.name}
                                    class="w-full h-full object-cover"
                                />
                            </div>
                            <div>
                                <div class="font-bold text-foreground">
                                    {client.name}
                                </div>
                                <div
                                    class="text-sm text-primary/80 font-medium"
                                >
                                    {client.role}
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        {/each}
    </div>
</section>
