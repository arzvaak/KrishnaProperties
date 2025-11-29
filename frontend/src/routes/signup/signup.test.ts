import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import SignupPage from './+page.svelte';

// Mock dependencies
vi.mock('$app/navigation', () => ({
    goto: vi.fn()
}));

vi.mock('$lib/firebase', () => ({
    auth: {}
}));

vi.mock('firebase/auth', () => ({
    GoogleAuthProvider: vi.fn(),
    signInWithPopup: vi.fn()
}));

vi.mock('svelte-sonner', () => ({
    toast: {
        error: vi.fn(),
        success: vi.fn()
    }
}));

// Mock fetchWithAuth
vi.mock('$lib/api', () => ({
    fetchWithAuth: vi.fn()
}));

describe('Signup Page', () => {
    it('renders phone input and signup button', () => {
        render(SignupPage);
        expect(screen.getByLabelText('Phone Number')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Sign up with Google/i })).toBeInTheDocument();
    });

    it('validates empty phone number', async () => {
        const { toast } = await import('svelte-sonner');
        render(SignupPage);

        const button = screen.getByRole('button', { name: /Sign up with Google/i });
        await fireEvent.click(button);

        expect(toast.error).toHaveBeenCalledWith('Please enter your phone number');
    });

    it('validates short phone number', async () => {
        const { toast } = await import('svelte-sonner');
        render(SignupPage);

        const input = screen.getByLabelText('Phone Number');
        await fireEvent.input(input, { target: { value: '123' } });

        const button = screen.getByRole('button', { name: /Sign up with Google/i });
        await fireEvent.click(button);

        expect(toast.error).toHaveBeenCalledWith('Please enter a valid Indian phone number (+91 followed by 10 digits)');
    });
});
