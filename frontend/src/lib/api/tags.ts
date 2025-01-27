import { API_URL, defaultHeaders } from './config';
import type { ApiTag, ApiBook } from '../types';

export async function fetchTags(): Promise<ApiTag[]> {
    const response = await fetch(`${API_URL}/tags`);
    if (!response.ok) {
        throw new Error('Failed to fetch tags');
    }
    return response.json();
}

export async function createTag(name: string): Promise<ApiTag> {
    const response = await fetch(`${API_URL}/tags`, {
        method: 'POST',
        headers: defaultHeaders,
        body: JSON.stringify({ name }),
    });
    if (!response.ok) {
        throw new Error('Failed to create tag');
    }
    return response.json();
}

export async function deleteTag(tagId: number): Promise<void> {
    const response = await fetch(`${API_URL}/tags/${tagId}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete tag');
    }
}

export async function addTagsToBook(bookId: number, tagNames: string[]): Promise<ApiBook> {
    const response = await fetch(`${API_URL}/books/${bookId}/tags`, {
        method: 'POST',
        headers: defaultHeaders,
        body: JSON.stringify({ tags: tagNames }),
    });
    if (!response.ok) {
        throw new Error('Failed to add tags to book');
    }
    return response.json();
}

export async function removeTagsFromBook(bookId: number, tagNames: string[]): Promise<ApiBook> {
    const response = await fetch(`${API_URL}/books/${bookId}/tags`, {
        method: 'DELETE',
        headers: defaultHeaders,
        body: JSON.stringify({ tags: tagNames }),
    });
    if (!response.ok) {
        throw new Error('Failed to remove tags from book');
    }
    return response.json();
}
