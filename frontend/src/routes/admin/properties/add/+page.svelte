<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";
    import {
        Card,
        CardContent,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card";
    import { toast } from "svelte-sonner";
    import { goto } from "$app/navigation";
    import { storage } from "$lib/firebase";
    import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
    import Map from "$lib/components/Map.svelte";

    let loading = false;
    let uploading = false;
    let files: File[] = [];
    let videoFile: File | null = null;
    let previewUrls: string[] = [];

    let formData = {
        title: "",
        location: "",
        price: "",
        type: "For Sale",
        bedrooms: "",
        bathrooms: "",
        area: "",
        description: "",
        imageUrl: "",
        images: [] as string[],
        videoUrl: "",
        videoType: "url" as "url" | "file",
        coordinates: { lat: 19.076, lng: 72.8777 },
    };

    function handleLocationSelect(lat: number, lng: number) {
        formData.coordinates = { lat, lng };
    }

    function handleFileChange(e: Event) {
        const target = e.target as HTMLInputElement;
        if (target.files) {
            files = Array.from(target.files);
            previewUrls = files.map((file) => URL.createObjectURL(file));
        }
    }

    function handleVideoChange(e: Event) {
        const target = e.target as HTMLInputElement;
        if (target.files && target.files[0]) {
            videoFile = target.files[0];
        }
    }

    async function uploadImages(): Promise<string[]> {
        if (files.length === 0) return [];

        const uploadPromises = files.map(async (file) => {
            const storageRef = ref(
                storage,
                `properties/${Date.now()}_${file.name}`,
            );
            await uploadBytes(storageRef, file);
            return await getDownloadURL(storageRef);
        });

        return await Promise.all(uploadPromises);
    }

    async function uploadVideo(): Promise<string> {
        if (!videoFile) return "";
        const storageRef = ref(
            storage,
            `properties/videos/${Date.now()}_${videoFile.name}`,
        );
        await uploadBytes(storageRef, videoFile);
        return await getDownloadURL(storageRef);
    }

    async function handleSubmit() {
        loading = true;
        try {
            if (files.length > 0) {
                uploading = true;
                const uploadedUrls = await uploadImages();
                formData.images = uploadedUrls;
                formData.imageUrl = uploadedUrls[0]; // Set first image as main image for backward compatibility

                if (formData.videoType === "file" && videoFile) {
                    formData.videoUrl = await uploadVideo();
                }

                uploading = false;
            } else if (formData.videoType === "file" && videoFile) {
                uploading = true;
                formData.videoUrl = await uploadVideo();
                uploading = false;
            }

            const response = await fetch(
                "http://127.0.0.1:5000/api/properties",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(formData),
                },
            );

            if (!response.ok) throw new Error("Failed to create property");

            toast.success("Property created successfully!");
            goto("/admin/properties");
        } catch (error: any) {
            toast.error(error.message);
        } finally {
            loading = false;
            uploading = false;
        }
    }
</script>

<div class="max-w-2xl mx-auto">
    <Card>
        <CardHeader>
            <CardTitle>Add New Property</CardTitle>
        </CardHeader>
        <CardContent class="space-y-6">
            <div class="space-y-2">
                <Label for="title">Property Title</Label>
                <Input
                    id="title"
                    bind:value={formData.title}
                    placeholder="e.g. Luxury Villa in Bandra"
                />
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label for="location">Location Name</Label>
                    <Input
                        id="location"
                        bind:value={formData.location}
                        placeholder="City, Area"
                    />
                </div>
                <div class="space-y-2">
                    <Label>Map Location (Click to set)</Label>
                    <div class="h-[200px] border rounded-md overflow-hidden">
                        <Map
                            lat={formData.coordinates.lat}
                            lng={formData.coordinates.lng}
                            interactive={true}
                            onLocationSelect={handleLocationSelect}
                        />
                    </div>
                </div>
                <div class="space-y-2">
                    <Label for="price">Price</Label>
                    <Input
                        id="price"
                        bind:value={formData.price}
                        placeholder="e.g. 12,50,00,000"
                    />
                </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
                <div class="space-y-2">
                    <Label for="bedrooms">Bedrooms</Label>
                    <Input
                        id="bedrooms"
                        type="number"
                        bind:value={formData.bedrooms}
                    />
                </div>
                <div class="space-y-2">
                    <Label for="bathrooms">Bathrooms</Label>
                    <Input
                        id="bathrooms"
                        type="number"
                        bind:value={formData.bathrooms}
                    />
                </div>
                <div class="space-y-2">
                    <Label for="area">Area (sqft)</Label>
                    <Input id="area" type="number" bind:value={formData.area} />
                </div>
            </div>

            <div class="space-y-2">
                <Label for="type">Type</Label>
                <select
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    bind:value={formData.type}
                >
                    <option value="For Sale">For Sale</option>
                    <option value="For Rent">For Rent</option>
                </select>
            </div>

            <div class="space-y-2">
                <Label for="description">Description</Label>
                <Textarea
                    id="description"
                    bind:value={formData.description}
                    placeholder="Detailed description of the property..."
                />
            </div>

            <div class="space-y-2">
                <Label for="image">Property Images</Label>
                <Input
                    id="image"
                    type="file"
                    accept="image/*"
                    multiple
                    onchange={handleFileChange}
                />
                {#if previewUrls.length > 0}
                    <div class="grid grid-cols-3 gap-2 mt-2">
                        {#each previewUrls as url}
                            <div
                                class="relative aspect-video w-full overflow-hidden rounded-md border"
                            >
                                <img
                                    src={url}
                                    alt="Preview"
                                    class="object-cover w-full h-full"
                                />
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>

            <div class="space-y-4 border-t pt-4">
                <Label>Property Video</Label>
                <div class="flex gap-4 mb-4">
                    <Button
                        type="button"
                        variant={formData.videoType === "url"
                            ? "default"
                            : "outline"}
                        onclick={() => (formData.videoType = "url")}
                    >
                        YouTube/Vimeo URL
                    </Button>
                    <Button
                        type="button"
                        variant={formData.videoType === "file"
                            ? "default"
                            : "outline"}
                        onclick={() => (formData.videoType = "file")}
                    >
                        Upload Video
                    </Button>
                </div>

                {#if formData.videoType === "url"}
                    <div class="space-y-2">
                        <Label for="videoUrl">Video URL</Label>
                        <Input
                            id="videoUrl"
                            bind:value={formData.videoUrl}
                            placeholder="https://www.youtube.com/watch?v=..."
                        />
                    </div>
                {:else}
                    <div class="space-y-2">
                        <Label for="videoFile">Upload Video File</Label>
                        <Input
                            id="videoFile"
                            type="file"
                            accept="video/*"
                            onchange={handleVideoChange}
                        />
                        <p class="text-xs text-muted-foreground">
                            Max size: 50MB. Supported formats: MP4, WebM.
                        </p>
                    </div>
                {/if}
            </div>

            <Button
                class="w-full"
                onclick={handleSubmit}
                disabled={loading || uploading}
            >
                {#if uploading}
                    Uploading Image...
                {:else if loading}
                    Creating Property...
                {:else}
                    Create Property
                {/if}
            </Button>
        </CardContent>
    </Card>
</div>
