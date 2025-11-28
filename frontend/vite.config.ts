import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
// import { sentrySvelteKit } from "@sentry/sveltekit/vite";

export default defineConfig({
	plugins: [
		// sentrySvelteKit({
		// 	sourceMapsUploadOptions: {
		// 		org: "de",
		// 		project: "javascript-sveltekit",
		// 	}
		// }),
		sveltekit()
	],
	build: {
		rollupOptions: {
			output: {
				manualChunks: {
					firebase: ['firebase/app', 'firebase/auth', 'firebase/firestore', 'firebase/storage'],
					ui: ['lucide-svelte', 'svelte-sonner']
				}
			}
		}
	}
});
