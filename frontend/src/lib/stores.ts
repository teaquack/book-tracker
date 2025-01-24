import { writable, derived } from 'svelte/store';

export interface Book {
    id: number;
    title: string;
    author: string;
    description?: string;
    list_id?: number;
}

export interface BookList {
    id: number;
    name: string;
    books: Book[];
}

// API response types
interface ApiBook {
    id: number;
    title: string;
    author: string;
    description?: string;
    list_id: number | null;
}

interface ApiBookList {
    id: number;
    name: string;
    books: ApiBook[];
}

export const lists = writable<BookList[]>([]);
export const books = writable<Book[]>([]);

// Derived store for unlisted books
export const unlistedBooks = derived([books], ([$books]) => {
    return $books.filter(book => !book.list_id);
});

// Derived store for books in a list
export const booksInList = (listId: number) => 
    derived([books], ([$books]) => {
        return $books.filter(book => book.list_id === listId);
    });

// API functions
const API_URL = 'http://127.0.0.1:5000';

// Initialize stores
export async function initializeStores() {
    try {
        const [listsData, booksData] = await Promise.all([
            fetchLists(),
            fetchBooks()
        ]);
        
        // Update the books store first
        const normalizedBooks: Book[] = booksData.map(book => ({
            ...book,
            list_id: book.list_id || undefined
        }));
        books.set(normalizedBooks);
        
        // Then update the lists store with the books from the books store
        const listsWithBooks: BookList[] = listsData.map(list => ({
            id: list.id,
            name: list.name,
            books: normalizedBooks.filter(book => book.list_id === list.id)
        }));
        lists.set(listsWithBooks);
    } catch (error) {
        console.error('Failed to initialize stores:', error);
    }
}

export async function fetchLists(): Promise<ApiBookList[]> {
    const response = await fetch(`${API_URL}/lists`);
    if (!response.ok) {
        throw new Error('Failed to fetch lists');
    }
    const data: ApiBookList[] = await response.json();
    return data;
}

export async function fetchBooks(): Promise<ApiBook[]> {
    const response = await fetch(`${API_URL}/books`);
    if (!response.ok) {
        throw new Error('Failed to fetch books');
    }
    const data: ApiBook[] = await response.json();
    return data;
}

export async function createList(name: string): Promise<BookList> {
    const response = await fetch(`${API_URL}/lists`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
    });
    if (!response.ok) {
        throw new Error('Failed to create list');
    }
    const newList: ApiBookList = await response.json();
    
    // Create the new list with empty books array
    const bookList: BookList = {
        id: newList.id,
        name: newList.name,
        books: []
    };

    // Immediately update the lists store
    lists.update(currentLists => {
        const updatedLists = [...currentLists, bookList];
        return updatedLists;
    });

    // Fetch fresh data in the background
    setTimeout(async () => {
        try {
            const [listsData, booksData] = await Promise.all([
                fetchLists(),
                fetchBooks()
            ]);

            // Update the books store
            const normalizedBooks: Book[] = booksData.map(book => ({
                ...book,
                list_id: book.list_id || undefined
            }));
            books.set(normalizedBooks);

            // Update the lists store
            const listsWithBooks: BookList[] = listsData.map(list => ({
                id: list.id,
                name: list.name,
                books: normalizedBooks.filter(book => book.list_id === list.id)
            }));
            lists.set(listsWithBooks);
        } catch (error) {
            console.error('Error refreshing data:', error);
        }
    }, 0);

    return bookList;
}

export async function createBook(book: Omit<Book, 'id'>, listId?: number): Promise<Book> {
    const response = await fetch(`${API_URL}/books`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...book, list_id: listId }),
    });
    if (!response.ok) {
        throw new Error('Failed to create book');
    }
    const newApiBook: ApiBook = await response.json();
    const newBook: Book = {
        ...newApiBook,
        list_id: newApiBook.list_id || undefined
    };
    
    // Update books store
    books.update(current => [...current, newBook]);
    
    // If the book was added to a list, update lists store
    if (listId) {
        lists.update(current => 
            current.map(list => 
                list.id === listId 
                    ? { ...list, books: [...list.books, newBook] }
                    : list
            )
        );
    }
    
    return newBook;
}

export async function addBookToList(listId: number, bookId: number): Promise<BookList> {
    const response = await fetch(`${API_URL}/lists/${listId}/books/${bookId}`, {
        method: 'POST',
    });
    if (!response.ok) {
        throw new Error('Failed to add book to list');
    }
    const updatedApiList: ApiBookList = await response.json();
    
    // Convert API books to our Book type
    const updatedBooks = updatedApiList.books.map(book => ({
        ...book,
        list_id: book.list_id || undefined
    }));
    
    const updatedList: BookList = {
        ...updatedApiList,
        books: updatedBooks
    };
    
    // Update the book's list_id in the books store
    books.update(current => 
        current.map(book => 
            book.id === bookId 
                ? { ...book, list_id: listId }
                : book
        )
    );
    
    // Update the lists store
    lists.update(current => 
        current.map(list => 
            list.id === listId 
                ? updatedList
                : {
                    ...list,
                    books: list.books.filter(book => book.id !== bookId)
                }
        )
    );
    
    return updatedList;
}

export async function updateBook(bookId: number, updates: Partial<Omit<Book, 'id' | 'list_id'>>): Promise<Book> {
    const response = await fetch(`${API_URL}/books/${bookId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
    });
    if (!response.ok) {
        throw new Error('Failed to update book');
    }
    const updatedApiBook: ApiBook = await response.json();
    const updatedBook: Book = {
        ...updatedApiBook,
        list_id: updatedApiBook.list_id || undefined
    };
    
    // Update books store
    books.update(current => 
        current.map(book => 
            book.id === bookId 
                ? updatedBook
                : book
        )
    );
    
    // Update lists store if book is in a list
    if (updatedBook.list_id) {
        lists.update(current =>
            current.map(list =>
                list.id === updatedBook.list_id
                    ? {
                        ...list,
                        books: list.books.map(book =>
                            book.id === bookId
                                ? updatedBook
                                : book
                        )
                    }
                    : list
            )
        );
    }
    
    return updatedBook;
}

export async function deleteBook(bookId: number): Promise<void> {
    const response = await fetch(`${API_URL}/books/${bookId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.message || 'Failed to delete book');
    }

    // Update the books store - this will automatically update unlistedBooks
    books.update(currentBooks => currentBooks.filter(book => book.id !== bookId));

    // Update any lists that might contain this book
    lists.update(currentLists => 
        currentLists.map(list => ({
            ...list,
            books: list.books.filter(book => book.id !== bookId)
        }))
    );
}

export async function deleteList(listId: number): Promise<void> {
    const response = await fetch(`${API_URL}/lists/${listId}`, {
        method: 'DELETE',
    });

    if (!response.ok) {
        throw new Error('Failed to delete list');
    }

    lists.update(currentLists => currentLists.filter(list => list.id !== listId));
    
    // Update books store to remove list_id from books in the deleted list
    books.update(currentBooks => 
        currentBooks.map(book => 
            book.list_id === listId 
                ? { ...book, list_id: undefined }
                : book
        )
    );
}
