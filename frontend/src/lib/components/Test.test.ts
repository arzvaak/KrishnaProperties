import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Test from './Test.svelte';

describe('Test Component', () => {
    it('renders', () => {
        render(Test, { props: { name: 'Vitest' } });
        expect(screen.getByText('Hello Vitest!')).toBeInTheDocument();
    });
});
