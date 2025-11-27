<script lang="ts">
    import { Card, CardContent } from "$lib/components/ui/card";

    export let price: number;
    export let interestRate = 8.5;
    export let downPaymentPercent = 20;

    $: monthlyPayment = Math.round(
        price * (1 - downPaymentPercent / 100) * (interestRate / 100 / 12),
    );
</script>

<Card class="border-none shadow-lg">
    <CardContent class="p-6">
        <h3 class="font-bold text-lg mb-2">Mortgage Estimator</h3>
        <p class="text-sm text-muted-foreground mb-4">
            Est. monthly payment ({downPaymentPercent}% down, {interestRate}%
            rate)
        </p>
        <div class="text-3xl font-bold text-primary">
            ₹ {monthlyPayment.toLocaleString()}
            <span class="text-sm font-normal text-muted-foreground">/ mo</span>
        </div>
    </CardContent>
</Card>
