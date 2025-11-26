<script>
  import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card";
  import { DollarSign, Users, Home } from "lucide-svelte";
</script>

<h1 class="text-3xl font-bold mb-8">Dashboard Overview</h1>

<div class="grid gap-4 md:grid-cols-3">
  <Card>
    <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle class="text-sm font-medium">Total Properties</CardTitle>
      <Home class="h-4 w-4 text-muted-foreground" />
    </CardHeader>
    <CardContent>
      <div class="text-2xl font-bold">12</div>
      <p class="text-xs text-muted-foreground">+2 from last month</p>
    </CardContent>
  </Card>
  
  <Card>
    <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle class="text-sm font-medium">Active Users</CardTitle>
      <Users class="h-4 w-4 text-muted-foreground" />
    </CardHeader>
    <CardContent>
      <div class="text-2xl font-bold">+573</div>
      <p class="text-xs text-muted-foreground">+201 since last hour</p>
    </CardContent>
  </Card>

  <Card>
    <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle class="text-sm font-medium">Total Revenue</CardTitle>
      <DollarSign class="h-4 w-4 text-muted-foreground" />
    </CardHeader>
    <CardContent>
      <div class="text-2xl font-bold">₹ 45.2L</div>
      <p class="text-xs text-muted-foreground">+19% from last month</p>
    </CardContent>
  </Card>
</div>
