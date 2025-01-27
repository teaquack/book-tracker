import { fetchBooks } from './books';
import { fetchLists } from './lists';
import { fetchTags } from './tags';

export * from './books';
export * from './lists';
export * from './tags';

// Initialize all stores
export async function initializeStores(): Promise<void> {
    await Promise.all([
        fetchLists(),
        fetchBooks(),
        fetchTags()
    ]);
}
