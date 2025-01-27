import { API_URL, defaultHeaders } from './config';
import type { ApiBook, Book } from '../types';

export async function fetchBooks(): Promise<ApiBook[]> {
    const response = await fetch(`${API_URL}/books`);
    if (!response.ok) {
        throw new Error('Failed to fetch books');
    }
    return response.json();
}

export async function createBook(data: Partial<Book>): Promise<ApiBook> {
    const response = await fetch(`${API_URL}/books`, {
        method: 'POST',
        headers: defaultHeaders,
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error('Failed to create book');
    }
    return response.json();
}

export async function updateBook(bookId: number, data: Partial<Book>): Promise<ApiBook> {
    const response = await fetch(`${API_URL}/books/${bookId}`, {
        method: 'PUT',
        headers: defaultHeaders,
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error('Failed to update book');
    }
    return response.json();
}

export async function deleteBook(bookId: number): Promise<void> {
    const response = await fetch(`${API_URL}/books/${bookId}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete book');
    }
}

export async function addBookToList(bookId: number, listId: number): Promise<ApiBook> {
    const response = await fetch(`${API_URL}/books/${bookId}/list/${listId}`, {
        method: 'PUT',
    });
    if (!response.ok) {
        throw new Error('Failed to add book to list');
    }
    return response.json();
}
