import { test, expect } from '@playwright/test';


test('login flow', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');

    // Check if login form is visible
    await expect(page.getByRole('heading', { name: 'Welcome Back' })).toBeVisible();

    // Check for Google login button
    await expect(page.getByRole('button', { name: 'Continue with Google' })).toBeVisible();
});
