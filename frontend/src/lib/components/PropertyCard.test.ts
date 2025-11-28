import { render, screen } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import PropertyCard from './PropertyCard.svelte';
import MockComponent from './MockComponent.svelte';

// Mock dependencies
vi.mock('$lib/stores/auth', () => ({
    user: { subscribe: (fn: any) => { fn(null); return () => { }; } }
}));

vi.mock('svelte-sonner', () => ({
    toast: {
        error: vi.fn(),
        success: vi.fn()
    }
}));

vi.mock('$lib/config', () => ({
    API_BASE_URL: 'http://localhost:5000'
}));

vi.mock('$lib/api', () => ({
    fetchWithAuth: vi.fn()
}));

// Inline mocks to avoid hoisting issues
vi.mock('$lib/components/ui/card', async () => {
    const Mock = (await import('./MockComponent.svelte')).default;
    return {
        Card: Mock, CardContent: Mock, CardFooter: Mock, CardHeader: Mock
    };
});

vi.mock('$lib/components/ui/button', async () => {
    const Mock = (await import('./MockComponent.svelte')).default;
    return { Button: Mock };
});

vi.mock('$lib/components/ui/badge', async () => {
    const Mock = (await import('./MockComponent.svelte')).default;
    return { Badge: Mock };
});

vi.mock('$lib/components/comparison/AddToCompareButton.svelte', async () => {
    const Mock = (await import('./MockComponent.svelte')).default;
    return { default: Mock };
});

vi.mock('lucide-svelte', async () => {
    const Mock = (await import('./MockComponent.svelte')).default;
    return {
        MapPin: Mock, Bed: Mock, Bath: Mock, Maximize: Mock, Heart: Mock
    };
});

describe('PropertyCard Component', () => {
    const mockProperty = {
        id: '1',
        title: 'Test Property',
        price: 1000000,
        location: 'Test Location',
        bedrooms: 3,
        bathrooms: 2,
        area: 1500,
        type: 'Apartment',
        images: ['test.jpg']
    };

    it('renders property details', () => {
        render(PropertyCard, { props: { property: mockProperty } });

        expect(screen.getByText('Test Property')).toBeInTheDocument();
        expect(screen.getByText('Test Location')).toBeInTheDocument();
        expect(screen.getByText('₹ 1000000')).toBeInTheDocument();
        expect(screen.getByText('3 Beds')).toBeInTheDocument();
        expect(screen.getByText('2 Baths')).toBeInTheDocument();
        expect(screen.getByText('1500 sqft')).toBeInTheDocument();
    });
});
