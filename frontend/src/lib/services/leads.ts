import { toast } from "svelte-sonner";
import { API_BASE_URL } from "$lib/config";
import { fetchWithAuth } from "$lib/api";

const API_BASE = `${API_BASE_URL}/api/admin/leads`;

export interface Lead {
    id: string;
    type: 'inquiry' | 'request';
    name?: string;
    email?: string;
    phone?: string;
    status: string;
    createdAt: string;
    title?: string;
    message?: string;
    property_id?: string;
    property_title?: string;
    criteria?: Record<string, any>;
    notes?: Note[];
    source?: string;
}

export interface Note {
    text: string;
    author: string;
    timestamp: string;
}

export async function fetchLeads(): Promise<Lead[]> {
    try {
        const res = await fetchWithAuth(API_BASE);
        if (!res.ok) throw new Error("Failed to fetch leads");
        return await res.json();
    } catch (error) {
        console.error(error);
        toast.error("Error loading leads");
        return [];
    }
}

export async function exportLeads() {
    try {
        const res = await fetchWithAuth(`${API_BASE}/export`);
        if (!res.ok) throw new Error("Failed to export leads");

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `leads_export_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success("Export started");
    } catch (error) {
        console.error(error);
        toast.error("Failed to export leads");
    }
}

export async function fetchLeadDetails(type: string, id: string): Promise<Lead | null> {
    try {
        const res = await fetchWithAuth(`${API_BASE}/${type}/${id}`);
        if (!res.ok) throw new Error("Failed to fetch lead details");
        return await res.json();
    } catch (error) {
        console.error(error);
        toast.error("Error loading lead");
        return null;
    }
}

export async function updateLeadStatus(type: string, id: string, status: string): Promise<boolean> {
    try {
        const res = await fetchWithAuth(`${API_BASE}/${type}/${id}`, {
            method: "PATCH",
            body: JSON.stringify({ status }),
        });
        if (!res.ok) throw new Error("Failed to update status");
        return true;
    } catch (error) {
        console.error(error);
        toast.error("Failed to update status");
        return false;
    }
}

export async function addLeadNote(type: string, id: string, text: string, author: string = "Admin"): Promise<Note | null> {
    try {
        const res = await fetchWithAuth(`${API_BASE}/${type}/${id}/notes`, {
            method: "POST",
            body: JSON.stringify({ text, author }),
        });
        if (!res.ok) throw new Error("Failed to add note");
        return await res.json();
    } catch (error) {
        console.error(error);
        toast.error("Failed to add note");
        return null;
    }
}
