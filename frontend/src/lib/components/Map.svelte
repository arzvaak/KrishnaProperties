<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import "leaflet/dist/leaflet.css";

    export let lat: number = 19.076; // Default to Mumbai
    export let lng: number = 72.8777;
    export let zoom: number = 13;
    export let interactive: boolean = false;
    export let onLocationSelect:
        | ((lat: number, lng: number) => void)
        | undefined = undefined;

    let mapElement: HTMLElement;
    let map: any;
    let marker: any;

    onMount(async () => {
        if (browser) {
            const L = (await import("leaflet")).default;

            map = L.map(mapElement).setView([lat, lng], zoom);

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution:
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            }).addTo(map);

            // Custom icon fix for Leaflet in SvelteKit/Vite
            const icon = L.icon({
                iconUrl:
                    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
                iconRetinaUrl:
                    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
                shadowUrl:
                    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41],
            });

            marker = L.marker([lat, lng], { icon }).addTo(map);

            if (interactive) {
                map.on("click", (e: any) => {
                    const { lat: newLat, lng: newLng } = e.latlng;
                    if (marker) {
                        marker.setLatLng([newLat, newLng]);
                    } else {
                        marker = L.marker([newLat, newLng], { icon }).addTo(
                            map,
                        );
                    }
                    if (onLocationSelect) {
                        onLocationSelect(newLat, newLng);
                    }
                });
            } else {
                map.dragging.disable();
                map.touchZoom.disable();
                map.doubleClickZoom.disable();
                map.scrollWheelZoom.disable();
                map.boxZoom.disable();
                map.keyboard.disable();
                if (map.tap) map.tap.disable();
            }
        }
    });

    onDestroy(() => {
        if (map) {
            map.remove();
        }
    });

    // Reactive update for lat/lng props
    $: if (
        map &&
        marker &&
        (lat !== marker.getLatLng().lat || lng !== marker.getLatLng().lng)
    ) {
        marker.setLatLng([lat, lng]);
        map.setView([lat, lng], zoom);
    }
</script>

<div bind:this={mapElement} class="w-full h-full rounded-lg z-0"></div>
