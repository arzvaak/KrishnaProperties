<script lang="ts">
  import { onMount } from "svelte";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Eye, Users, Home, MessageSquare, Activity } from "lucide-svelte";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import DashboardCharts from "$lib/components/DashboardCharts.svelte";
  import { API_BASE_URL } from "$lib/config";
  import { fetchWithAuth } from "$lib/api";

  let stats: any = null;
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      const response = await fetchWithAuth(
        `${API_BASE_URL}/api/analytics/dashboard`,
      );
      if (!response.ok) throw new Error("Failed to fetch dashboard stats");
      stats = await response.json();
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  function formatDate(isoString: string) {
    return new Date(isoString).toLocaleString();
  }
</script>

<div class="space-y-8">
  <div>
    <h1 class="text-3xl font-bold tracking-tight">Dashboard</h1>
    <p class="text-muted-foreground">Overview of your website's performance.</p>
  </div>

  {#if loading}
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {#each Array(4) as _}
        <Skeleton class="h-32 rounded-xl" />
      {/each}
    </div>
  {:else if error}
    <div class="text-red-500">Error: {error}</div>
  {:else if stats}
    <!-- Stats Cards -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Total Users</CardTitle>
          <Users class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{stats.total_users}</div>
          <p class="text-xs text-muted-foreground">Registered accounts</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Total Leads</CardTitle>
          <MessageSquare class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{stats.total_leads}</div>
          <p class="text-xs text-muted-foreground">Inquiries & Requests</p>
        </CardContent>
      </Card>
    </div>

    <!-- Charts Section -->
    <DashboardCharts
      trafficStats={stats.traffic_stats || []}
      funnel={stats.funnel || {}}
      topProperties={stats.most_viewed_properties || []}
    />

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <!-- Existing Cards (Site Views, Properties) -->
      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Total Site Views</CardTitle>
          <Eye class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{stats.site_views}</div>
          <p class="text-xs text-muted-foreground">+20.1% from last month</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Total Properties</CardTitle>
          <Home class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{stats.total_properties}</div>
          <p class="text-xs text-muted-foreground">+2 new this week</p>
        </CardContent>
      </Card>

      <!-- Recent Activity -->
      <Card class="col-span-4">
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-8">
            {#each stats.recent_events as event}
              <div class="flex items-center">
                <div
                  class="h-9 w-9 rounded-full bg-primary/10 flex items-center justify-center mr-4"
                >
                  <Activity class="h-4 w-4 text-primary" />
                </div>
                <div class="space-y-1">
                  <p class="text-sm font-medium leading-none">
                    {#if event.type === "site_view"}
                      New Website Visit
                    {:else if event.type === "property_view"}
                      Property Viewed (ID: {event.property_id})
                    {:else if event.type === "contact"}
                      New Contact Inquiry from {event.metadata?.name || "User"}
                    {:else}
                      {event.type}
                    {/if}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    {formatDate(event.timestamp)}
                  </p>
                </div>
              </div>
            {/each}
            {#if stats.recent_events.length === 0}
              <p class="text-muted-foreground text-sm">No recent activity.</p>
            {/if}
          </div>
        </CardContent>
      </Card>
    </div>
  {/if}
</div>
