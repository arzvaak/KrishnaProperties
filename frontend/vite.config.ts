import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		environment: 'jsdom',
		globals: true,
		setupFiles: ['src/setupTest.ts'],
	},
	resolve: {
		conditions: ['browser']
	},
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
