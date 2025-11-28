<script lang="ts">
  import { settings } from "$lib/stores/settings";
  import {
    Facebook,
    Twitter,
    Instagram,
    Linkedin,
    Youtube,
    Mail,
    Phone,
    MapPin,
  } from "lucide-svelte";
</script>

<footer class="bg-muted/50 border-t py-12 mt-auto">
  <div class="container grid grid-cols-1 md:grid-cols-4 gap-8">
    <div class="space-y-4">
      <h3 class="font-bold text-lg">{$settings.general.siteName}</h3>
      <p class="text-sm text-muted-foreground">
        {$settings.general.tagline}
      </p>
      <div class="flex gap-4">
        {#if $settings.social.facebook}
          <a
            href={$settings.social.facebook}
            target="_blank"
            rel="noopener noreferrer"
            class="text-muted-foreground hover:text-primary"
          >
            <Facebook class="h-5 w-5" />
          </a>
        {/if}
        {#if $settings.social.twitter}
          <a
            href={$settings.social.twitter}
            target="_blank"
            rel="noopener noreferrer"
            class="text-muted-foreground hover:text-primary"
          >
            <Twitter class="h-5 w-5" />
          </a>
        {/if}
        {#if $settings.social.instagram}
          <a
            href={$settings.social.instagram}
            target="_blank"
            rel="noopener noreferrer"
            class="text-muted-foreground hover:text-primary"
          >
            <Instagram class="h-5 w-5" />
          </a>
        {/if}
        {#if $settings.social.linkedin}
          <a
            href={$settings.social.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            class="text-muted-foreground hover:text-primary"
          >
            <Linkedin class="h-5 w-5" />
          </a>
        {/if}
        {#if $settings.social.youtube}
          <a
            href={$settings.social.youtube}
            target="_blank"
            rel="noopener noreferrer"
            class="text-muted-foreground hover:text-primary"
          >
            <Youtube class="h-5 w-5" />
          </a>
        {/if}
      </div>
    </div>

    <div>
      <h4 class="font-semibold mb-4">Quick Links</h4>
      <ul class="space-y-2 text-sm text-muted-foreground">
        <li><a href="/properties" class="hover:text-primary">Properties</a></li>
        <li><a href="/blog" class="hover:text-primary">Blog</a></li>
        <li><a href="/contact" class="hover:text-primary">Contact Us</a></li>
        <li><a href="/about" class="hover:text-primary">About Us</a></li>
      </ul>
    </div>

    <div>
      <h4 class="font-semibold mb-4">Contact Us</h4>
      <ul class="space-y-3 text-sm text-muted-foreground">
        <li class="flex items-start gap-2">
          <MapPin class="h-4 w-4 mt-0.5 shrink-0" />
          <span>{$settings.contact.address}</span>
        </li>
        <li class="flex items-center gap-2">
          <Phone class="h-4 w-4 shrink-0" />
          <a href="tel:{$settings.contact.phone}" class="hover:text-primary"
            >{$settings.contact.phone}</a
          >
        </li>
        <li class="flex items-center gap-2">
          <Mail class="h-4 w-4 shrink-0" />
          <a href="mailto:{$settings.contact.email}" class="hover:text-primary"
            >{$settings.contact.email}</a
          >
        </li>
      </ul>
    </div>

    <div>
      <h4 class="font-semibold mb-4">Legal</h4>
      <ul class="space-y-2 text-sm text-muted-foreground">
        <li>
          <a href="/privacy" class="hover:text-primary">Privacy Policy</a>
        </li>
        <li>
          <a href="/terms" class="hover:text-primary">Terms of Service</a>
        </li>
      </ul>
    </div>
  </div>
</footer>
