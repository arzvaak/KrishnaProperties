import { writable } from 'svelte/store';

export interface Settings {
    general: {
        siteName: string;
        tagline: string;
        logo: string;
    };
    contact: {
        email: string;
        phone: string;
        address: string;
        mapEmbedUrl: string;
    };
    social: {
        facebook: string;
        twitter: string;
        instagram: string;
        linkedin: string;
        youtube: string;
    };
    seo: {
        defaultTitle: string;
        defaultDescription: string;
        defaultKeywords: string;
    };
}

const defaultSettings: Settings = {
    general: {
        siteName: "Krishna Properties",
        tagline: "Your Dream Home Awaits",
        logo: ""
    },
    contact: {
        email: "info@krishnaproperties.com",
        phone: "+91 98765 43210",
        address: "123, Real Estate Avenue, Mumbai, India",
        mapEmbedUrl: ""
    },
    social: {
        facebook: "",
        twitter: "",
        instagram: "",
        linkedin: "",
        youtube: ""
    },
    seo: {
        defaultTitle: "Krishna Properties - Premium Real Estate",
        defaultDescription: "Find your dream home with Krishna Properties. We offer the best luxury apartments, villas, and plots.",
        defaultKeywords: "real estate, luxury homes, apartments, villas, buy property"
    }
};

export const settings = writable<Settings>(defaultSettings);
