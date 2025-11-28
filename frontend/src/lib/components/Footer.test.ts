import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Footer from './Footer.svelte';

describe('Footer Component', () => {
    it('renders company name', () => {
        render(Footer);
        expect(screen.getByText('Krishna Properties')).toBeInTheDocument();
    });

    it('renders quick links', () => {
        render(Footer);
        expect(screen.getByText('Properties')).toBeInTheDocument();
        expect(screen.getByText('Agents')).toBeInTheDocument();
        expect(screen.getByText('About Us')).toBeInTheDocument();
    });

    it('renders legal links', () => {
        render(Footer);
        expect(screen.getByText('Privacy Policy')).toBeInTheDocument();
        expect(screen.getByText('Terms of Service')).toBeInTheDocument();
    });
});
