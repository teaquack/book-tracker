import { writable, derived } from 'svelte/store';
import type { Book, ApiBook } from '../types';
import * as api from '../api';

// Store
export const books = writable<Book[]>([]);

// Derived stores
export const unlistedBooks = derived(books, $books => {
    return $books.filter(book => !book.list_id);
});

export const getBooksByList = (listId: number) => derived(books, $books => {
    return $books.filter(book => book.list_id === listId);
});

// Helper functions
function convertApiBook(apiBook: ApiBook): Book {
    return {
        ...apiBook,
        list_id: apiBook.list_id || undefined,
        description: apiBook.description || undefined
    };
}

// Store actions
export async function fetchBooks(): Promise<Book[]> {
    const apiBooks = await api.fetchBooks();
    const convertedBooks = apiBooks.map(convertApiBook);
    books.set(convertedBooks);
    return convertedBooks;
}

export async function createBook(data: Partial<Book>): Promise<Book> {
    const apiBook = await api.createBook(data);
    const book = convertApiBook(apiBook);
    books.update(current => [...current, book]);
    return book;
}

export async function updateBook(bookId: number, data: Partial<Book>): Promise<Book> {
    const apiBook = await api.updateBook(bookId, data);
    const book = convertApiBook(apiBook);
    books.update(current => 
        current.map(b => b.id === bookId ? book : b)
    );
    return book;
}

export async function deleteBook(bookId: number): Promise<void> {
    await api.deleteBook(bookId);
    books.update(current => current.filter(book => book.id !== bookId));
}

export async function addBookToList(bookId: number, listId: number): Promise<Book> {
    const apiBook = await api.addBookToList(bookId, listId);
    const book = convertApiBook(apiBook);
    books.update(current => 
        current.map(b => b.id === bookId ? book : b)
    );
    return book;
}

export async function addTagsToBook(bookId: number, tagNames: string[]): Promise<Book> {
    const apiBook = await api.addTagsToBook(bookId, tagNames);
    const book = convertApiBook(apiBook);
    books.update(current => 
        current.map(b => b.id === bookId ? book : b)
    );
    return book;
}

export async function removeTagsFromBook(bookId: number, tagNames: string[]): Promise<Book> {
    const apiBook = await api.removeTagsFromBook(bookId, tagNames);
    const book = convertApiBook(apiBook);
    books.update(current => 
        current.map(b => b.id === bookId ? book : b)
    );
    return book;
}
