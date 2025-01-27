import { API_URL, defaultHeaders } from './config';
import type { ApiList } from '../types';

export async function fetchLists(): Promise<ApiList[]> {
    const response = await fetch(`${API_URL}/lists`);
    if (!response.ok) {
        throw new Error('Failed to fetch lists');
    }
    return response.json();
}

export async function createList(name: string): Promise<ApiList> {
    const response = await fetch(`${API_URL}/lists`, {
        method: 'POST',
        headers: defaultHeaders,
        body: JSON.stringify({ name }),
    });
    if (!response.ok) {
        throw new Error('Failed to create list');
    }
    return response.json();
}

export async function deleteList(listId: number): Promise<void> {
    const response = await fetch(`${API_URL}/lists/${listId}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete list');
    }
}
