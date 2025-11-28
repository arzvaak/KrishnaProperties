import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import Button from './button.svelte';

describe('Button Component', () => {
    it('renders', () => {
        render(Button);
        const btn = screen.getByRole('button');
        expect(btn).toBeInTheDocument();
    });

    it('handles click events', async () => {
        const handleClick = vi.fn();
        render(Button, { props: { onclick: handleClick } });

        const btn = screen.getByRole('button');
        await fireEvent.click(btn);

        expect(handleClick).toHaveBeenCalled();
    });
});
