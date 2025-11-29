<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import {
        Card,
        CardContent,
        CardDescription,
        CardHeader,
        CardTitle,
        CardFooter,
    } from "$lib/components/ui/card";
    import { auth } from "$lib/firebase";
    import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
    import { goto } from "$app/navigation";
    import { toast } from "svelte-sonner";
    import { API_BASE_URL } from "$lib/config";
    import { fetchWithAuth } from "$lib/api";

    let phoneNumber = "";
    let isLoading = false;

    async function handleGoogleSignup() {
        if (!phoneNumber) {
            toast.error("Please enter your phone number");
            return;
        }

        // Validate Indian Phone Number (+91XXXXXXXXXX)
        const phoneRegex = /^\+91\d{10}$/;
        if (!phoneRegex.test(phoneNumber)) {
            toast.error(
                "Please enter a valid Indian phone number (+91 followed by 10 digits)",
            );
            return;
        }

        isLoading = true;
        try {
            const provider = new GoogleAuthProvider();
            await signInWithPopup(auth, provider);

            // Sync user with backend, including phone number
            await fetchWithAuth(`${API_BASE_URL}/api/users/sync`, {
                method: "POST",
                body: JSON.stringify({ phoneNumber }),
            });

            toast.success("Account created successfully!");
            goto("/");
        } catch (error: any) {
            console.error("Signup error:", error);
            toast.error(error.message || "Failed to sign up");
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="flex items-center justify-center min-h-[80vh] px-4 pt-24">
    <Card class="w-full max-w-md">
        <CardHeader class="text-center">
            <CardTitle class="text-2xl">Create an Account</CardTitle>
            <CardDescription
                >Sign up to get started with Krishna Properties</CardDescription
            >
        </CardHeader>
        <CardContent class="space-y-6">
            <div class="space-y-2">
                <Label for="phone">Phone Number</Label>
                <Input
                    id="phone"
                    type="tel"
                    placeholder="+91 98765 43210"
                    bind:value={phoneNumber}
                />
                <p class="text-xs text-muted-foreground">
                    We'll use this to contact you about property inquiries.
                </p>
            </div>

            <Button
                variant="outline"
                class="w-full py-6 text-base"
                onclick={handleGoogleSignup}
                disabled={isLoading}
            >
                {#if isLoading}
                    <span class="mr-2">Signing up...</span>
                {:else}
                    <svg class="mr-2 h-5 w-5" viewBox="0 0 24 24">
                        <path
                            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                            fill="#4285F4"
                        />
                        <path
                            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                            fill="#34A853"
                        />
                        <path
                            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                            fill="#FBBC05"
                        />
                        <path
                            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                            fill="#EA4335"
                        />
                    </svg>
                    Sign up with Google
                {/if}
            </Button>
        </CardContent>
        <CardFooter class="justify-center">
            <div class="text-sm text-muted-foreground">
                Already have an account? <a
                    href="/login"
                    class="text-primary hover:underline">Log in</a
                >
            </div>
        </CardFooter>
    </Card>
</div>
