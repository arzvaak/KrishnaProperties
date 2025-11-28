<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import * as Select from "$lib/components/ui/select";
    import { Textarea } from "$lib/components/ui/textarea";
    import * as Tabs from "$lib/components/ui/tabs";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
        CardDescription,
    } from "$lib/components/ui/card";
    import { toast } from "svelte-sonner";
    import { user } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import {
        Sparkles,
        Home,
        MapPin,
        Clock,
        Search,
        Key,
        ShieldCheck,
        ArrowRight,
    } from "lucide-svelte";
    import { reveal } from "$lib/actions/reveal";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let loading = false;

    // Form State
    let propertyType = "any";
    let location = "";
    let minPrice = "";
    let maxPrice = "";
    let bedrooms = "any";
    let bathrooms = "any";
    let timeline = "immediate";
    let requirements = "";

    async function handleSubmit() {
        if (!$user) {
            toast.error("Please log in to submit a request.");
            goto("/login");
            return;
        }

        loading = true;
        try {
            const criteria = {
                type: propertyType,
                location,
                minPrice: minPrice ? parseInt(minPrice) : 0,
                maxPrice: maxPrice ? parseInt(maxPrice) : 1000000000,
                bedrooms: bedrooms === "any" ? 0 : parseInt(bedrooms),
                bathrooms: bathrooms === "any" ? 0 : parseInt(bathrooms),
                timeline,
                requirements,
            };

            const res = await fetchWithAuth(`${API_BASE_URL}/api/requests`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: $user.uid,
                    criteria,
                }),
            });

            if (!res.ok) throw new Error("Failed to submit request");

            toast.success(
                "Request submitted! We'll notify you when we find a match.",
            );
            goto("/my-activity");
        } catch (error) {
            console.error(error);
            toast.error("Failed to submit request. Please try again.");
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-screen bg-background">
    <!-- Hero Section -->
    <div class="relative h-[500px] bg-black overflow-hidden">
        <div
            class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2053&q=80')] bg-cover bg-center opacity-50"
        ></div>
        <div
            class="absolute inset-0 bg-gradient-to-t from-background via-background/20 to-transparent"
        ></div>
        <div
            class="container relative h-full flex flex-col justify-center items-center text-center text-white px-4"
            use:reveal
        >
            <div
                class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 mb-6"
            >
                <Sparkles class="w-4 h-4 text-amber-400" />
                <span class="font-medium text-amber-100"
                    >Premium Concierge Service</span
                >
            </div>
            <h1 class="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
                Your Dream Home, <br /> Found for You.
            </h1>
            <p class="text-xl text-gray-200 max-w-2xl leading-relaxed">
                Can't find what you're looking for? Tell us your exact
                requirements, and our team will access exclusive off-market
                listings to find your perfect match.
            </p>
        </div>
    </div>

    <!-- How It Works -->
    <section class="py-20 container px-4">
        <div class="text-center mb-16" use:reveal>
            <h2 class="text-3xl font-bold mb-4">How It Works</h2>
            <p class="text-muted-foreground max-w-xl mx-auto">
                We simplify your property search with a personalized approach.
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
            <!-- Connecting Line (Desktop) -->
            <div
                class="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-border -z-10"
            ></div>

            <div
                class="text-center bg-background pt-4"
                use:reveal={{ delay: 0 }}
            >
                <div
                    class="w-24 h-24 mx-auto bg-primary/10 rounded-full flex items-center justify-center mb-6 shadow-sm"
                >
                    <Search class="w-10 h-10 text-primary" />
                </div>
                <h3 class="text-xl font-bold mb-3">1. Share Requirements</h3>
                <p class="text-muted-foreground">
                    Fill out the form below with your specific needs, budget,
                    and preferences.
                </p>
            </div>
            <div
                class="text-center bg-background pt-4"
                use:reveal={{ delay: 100 }}
            >
                <div
                    class="w-24 h-24 mx-auto bg-primary/10 rounded-full flex items-center justify-center mb-6 shadow-sm"
                >
                    <Key class="w-10 h-10 text-primary" />
                </div>
                <h3 class="text-xl font-bold mb-3">2. We Search for You</h3>
                <p class="text-muted-foreground">
                    Our agents scan the market, including private listings not
                    available online.
                </p>
            </div>
            <div
                class="text-center bg-background pt-4"
                use:reveal={{ delay: 200 }}
            >
                <div
                    class="w-24 h-24 mx-auto bg-primary/10 rounded-full flex items-center justify-center mb-6 shadow-sm"
                >
                    <ShieldCheck class="w-10 h-10 text-primary" />
                </div>
                <h3 class="text-xl font-bold mb-3">3. Curated Selection</h3>
                <p class="text-muted-foreground">
                    Receive a shortlist of properties that match your criteria
                    perfectly.
                </p>
            </div>
        </div>
    </section>

    <!-- Form Section -->
    <section class="pb-32 container px-4" use:reveal>
        <div class="grid lg:grid-cols-3 gap-12">
            <!-- Benefits Sidebar -->
            <div class="lg:col-span-1 space-y-8">
                <div class="bg-primary/5 rounded-3xl p-8 space-y-6">
                    <h3 class="text-2xl font-bold">Why Use This Service?</h3>
                    <ul class="space-y-4">
                        <li class="flex gap-3">
                            <div
                                class="mt-1 w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0"
                            >
                                <ArrowRight class="w-3 h-3 text-primary" />
                            </div>
                            <div>
                                <h4 class="font-semibold">Save Time</h4>
                                <p class="text-sm text-muted-foreground">
                                    Stop scrolling endlessly. Let us do the
                                    heavy lifting.
                                </p>
                            </div>
                        </li>
                        <li class="flex gap-3">
                            <div
                                class="mt-1 w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0"
                            >
                                <ArrowRight class="w-3 h-3 text-primary" />
                            </div>
                            <div>
                                <h4 class="font-semibold">Off-Market Access</h4>
                                <p class="text-sm text-muted-foreground">
                                    Get access to properties before they hit the
                                    public portals.
                                </p>
                            </div>
                        </li>
                        <li class="flex gap-3">
                            <div
                                class="mt-1 w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0"
                            >
                                <ArrowRight class="w-3 h-3 text-primary" />
                            </div>
                            <div>
                                <h4 class="font-semibold">
                                    Expert Negotiation
                                </h4>
                                <p class="text-sm text-muted-foreground">
                                    Our agents help you get the best price
                                    possible.
                                </p>
                            </div>
                        </li>
                    </ul>
                </div>

                <div
                    class="bg-black text-white rounded-3xl p-8 text-center space-y-4"
                >
                    <h3 class="text-xl font-bold">Prefer to talk?</h3>
                    <p class="text-gray-400">
                        Our experts are available 24/7 to discuss your needs.
                    </p>
                    <Button
                        variant="secondary"
                        class="w-full rounded-full"
                        href="/contact"
                    >
                        Contact Us
                    </Button>
                </div>
            </div>

            <!-- Main Form -->
            <div class="lg:col-span-2">
                <Card class="border-none shadow-2xl overflow-hidden">
                    <div
                        class="h-2 bg-gradient-to-r from-amber-400 to-primary"
                    ></div>
                    <CardHeader class="p-8 pb-0">
                        <CardTitle class="text-3xl">
                            Tell Us What You Need
                        </CardTitle>
                        <CardDescription class="text-lg">
                            Complete the form below to start your personalized
                            search.
                        </CardDescription>
                    </CardHeader>
                    <CardContent class="p-8 space-y-8">
                        <!-- Transaction Type Removed -->
                        <!-- <div class="flex justify-center pb-6 border-b">
                             Tabs were here
                        </div> -->

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <!-- Property Details -->
                            <div class="space-y-6">
                                <div
                                    class="flex items-center gap-2 text-lg font-semibold text-primary"
                                >
                                    <Home class="w-5 h-5" />
                                    <h3>Property Details</h3>
                                </div>

                                <div class="space-y-4">
                                    <div class="space-y-2">
                                        <Label>Property Type</Label>
                                        <Select.Root
                                            type="single"
                                            bind:value={propertyType}
                                        >
                                            <Select.Trigger class="w-full h-12">
                                                <span class="capitalize"
                                                    >{propertyType === "any"
                                                        ? "Any Type"
                                                        : propertyType}</span
                                                >
                                            </Select.Trigger>
                                            <Select.Content>
                                                <Select.Item value="any"
                                                    >Any Type</Select.Item
                                                >
                                                <Select.Item
                                                    value="Authority plots"
                                                    >Authority plots</Select.Item
                                                >
                                                <Select.Item
                                                    value="Free Hold plots"
                                                    >Free Hold plots</Select.Item
                                                >
                                                <Select.Item
                                                    value="Commercial Plots"
                                                    >Commercial Plots</Select.Item
                                                >
                                                <Select.Item
                                                    value="Industrial or Factory Plots"
                                                    >Industrial or Factory Plots</Select.Item
                                                >
                                                <Select.Item value="Villa's"
                                                    >Villa's</Select.Item
                                                >
                                            </Select.Content>
                                        </Select.Root>
                                    </div>

                                    <div class="grid grid-cols-2 gap-4">
                                        <div class="space-y-2">
                                            <Label>Bedrooms</Label>
                                            <Select.Root
                                                type="single"
                                                bind:value={bedrooms}
                                            >
                                                <Select.Trigger class="h-12">
                                                    {bedrooms === "any"
                                                        ? "Any"
                                                        : `${bedrooms}+ BHK`}
                                                </Select.Trigger>
                                                <Select.Content>
                                                    <Select.Item value="any"
                                                        >Any</Select.Item
                                                    >
                                                    <Select.Item value="1"
                                                        >1+ BHK</Select.Item
                                                    >
                                                    <Select.Item value="2"
                                                        >2+ BHK</Select.Item
                                                    >
                                                    <Select.Item value="3"
                                                        >3+ BHK</Select.Item
                                                    >
                                                    <Select.Item value="4"
                                                        >4+ BHK</Select.Item
                                                    >
                                                    <Select.Item value="5"
                                                        >5+ BHK</Select.Item
                                                    >
                                                </Select.Content>
                                            </Select.Root>
                                        </div>
                                        <div class="space-y-2">
                                            <Label>Bathrooms</Label>
                                            <Select.Root
                                                type="single"
                                                bind:value={bathrooms}
                                            >
                                                <Select.Trigger class="h-12">
                                                    {bathrooms === "any"
                                                        ? "Any"
                                                        : `${bathrooms}+`}
                                                </Select.Trigger>
                                                <Select.Content>
                                                    <Select.Item value="any"
                                                        >Any</Select.Item
                                                    >
                                                    <Select.Item value="1"
                                                        >1+</Select.Item
                                                    >
                                                    <Select.Item value="2"
                                                        >2+</Select.Item
                                                    >
                                                    <Select.Item value="3"
                                                        >3+</Select.Item
                                                    >
                                                    <Select.Item value="4"
                                                        >4+</Select.Item
                                                    >
                                                </Select.Content>
                                            </Select.Root>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Location & Budget -->
                            <div class="space-y-6">
                                <div
                                    class="flex items-center gap-2 text-lg font-semibold text-primary"
                                >
                                    <MapPin class="w-5 h-5" />
                                    <h3>Location & Budget</h3>
                                </div>

                                <div class="space-y-4">
                                    <div class="space-y-2">
                                        <Label>Preferred Location</Label>
                                        <Input
                                            class="h-12"
                                            placeholder="e.g. Bandra West, Juhu, Powai"
                                            bind:value={location}
                                        />
                                    </div>

                                    <div class="space-y-2">
                                        <Label>Budget Range (₹)</Label>
                                        <div class="grid grid-cols-2 gap-4">
                                            <Input
                                                class="h-12"
                                                type="number"
                                                placeholder="Min"
                                                bind:value={minPrice}
                                            />
                                            <Input
                                                class="h-12"
                                                type="number"
                                                placeholder="Max"
                                                bind:value={maxPrice}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Timeline & Additional -->
                        <div class="space-y-6 pt-6 border-t">
                            <div
                                class="flex items-center gap-2 text-lg font-semibold text-primary"
                            >
                                <Clock class="w-5 h-5" />
                                <h3>Timeline & Preferences</h3>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <div class="space-y-2">
                                    <Label>When are you planning to buy?</Label>
                                    <Select.Root
                                        type="single"
                                        bind:value={timeline}
                                    >
                                        <Select.Trigger class="h-12">
                                            <span class="capitalize"
                                                >{timeline.replace(
                                                    "-",
                                                    " ",
                                                )}</span
                                            >
                                        </Select.Trigger>
                                        <Select.Content>
                                            <Select.Item value="immediate"
                                                >Immediately</Select.Item
                                            >
                                            <Select.Item value="1-3-months"
                                                >Within 1-3 Months</Select.Item
                                            >
                                            <Select.Item value="3-6-months"
                                                >Within 3-6 Months</Select.Item
                                            >
                                            <Select.Item value="6-plus-months"
                                                >After 6 Months</Select.Item
                                            >
                                            <Select.Item value="exploring"
                                                >Just Exploring</Select.Item
                                            >
                                        </Select.Content>
                                    </Select.Root>
                                </div>

                                <div class="space-y-2">
                                    <Label>Additional Requirements</Label>
                                    <Textarea
                                        placeholder="Tell us about specific amenities, facing, floor preference, or any other requirements..."
                                        class="h-32 resize-none"
                                        bind:value={requirements}
                                    />
                                </div>
                            </div>
                        </div>

                        <div class="pt-6">
                            <Button
                                size="lg"
                                class="w-full text-lg h-14 rounded-full shadow-lg hover:shadow-xl transition-all"
                                onclick={handleSubmit}
                                disabled={loading}
                            >
                                {loading
                                    ? "Submitting Request..."
                                    : "Submit Property Request"}
                            </Button>
                            <p
                                class="text-center text-sm text-muted-foreground mt-4"
                            >
                                By submitting this form, you agree to be
                                contacted by our agents regarding your property
                                search.
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </section>
</div>
