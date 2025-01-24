<script lang="ts">
    import { onMount } from 'svelte';
    import { lists, unlistedBooks, addBookToList, initializeStores } from './stores';

    type BookWithSelect = {
        id: number;
        title: string;
        author: string;
        description?: string;
        selectElement?: HTMLSelectElement;
    };

    async function addToList(bookId: number, select: HTMLSelectElement) {
        if (!select.value) return;
        
        try {
            await addBookToList(parseInt(select.value), bookId);
            select.value = ''; // Reset the select after adding
        } catch (e) {
            console.error('Failed to add book to list:', e);
        }
    }

    // Initialize data on mount
    onMount(async () => {
        await initializeStores();
    });

    // Cast unlisted books to include selectElement
    $: booksWithSelect = $unlistedBooks.map(book => ({
        ...book,
        selectElement: undefined
    })) as BookWithSelect[];
</script>

<div class="book-list unlisted-books">
    <h2>Unlisted Books</h2>
    <div class="books">
        {#if booksWithSelect.length === 0}
            <p class="empty">No unlisted books</p>
        {/if}
        {#each booksWithSelect as book (book.id)}
            <div class="book-card">
                <div class="book-content">
                    <h3>{book.title}</h3>
                    <p class="author">by {book.author}</p>
                    {#if book.description}
                        <p class="description">{book.description}</p>
                    {/if}
                </div>
                <div class="add-to-list">
                    <select 
                        bind:this={book.selectElement}
                        value=""
                    >
                        <option value="" disabled>Select a list...</option>
                        {#each $lists as list}
                            <option value={list.id}>{list.name}</option>
                        {/each}
                    </select>
                    <button 
                        class="add-button"
                        on:click={() => book.selectElement && addToList(book.id, book.selectElement)}
                    >
                        Add to List
                    </button>
                </div>
            </div>
        {/each}
    </div>
</div>
