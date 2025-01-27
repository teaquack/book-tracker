<script lang="ts">
    import { onMount } from 'svelte';
    import { lists, unlistedBooks, addBookToList, initializeStores, updateBook, deleteBook } from './stores/index';
    import type { Book } from './types';

    // Map to store select elements
    const selectElements = new Map<number, HTMLSelectElement>();

    // Simple editing state
    let editingId: number | null = null;
    let editTitle = '';
    let editAuthor = '';
    let editDescription = '';

    function startEdit(book: Book) {
        editingId = book.id;
        editTitle = book.title;
        editAuthor = book.author;
        editDescription = book.description || '';
    }

    function cancelEdit() {
        editingId = null;
    }

    async function saveEdit() {
        if (!editingId) return;

        try {
            await updateBook(editingId, {
                title: editTitle,
                author: editAuthor,
                description: editDescription
            });
            editingId = null;
        } catch (e) {
            console.error('Failed to update book:', e);
        }
    }

    async function handleDelete(book: Book) {
        if (!confirm(`Are you sure you want to permanently delete "${book.title}"? This cannot be undone.`)) {
            return;
        }

        try {
            await deleteBook(book.id);
        } catch (e) {
            console.error('Failed to delete book:', e);
        }
    }

    async function addToList(bookId: number) {
        const select = selectElements.get(bookId);
        if (!select?.value) return;
        
        try {
            await addBookToList(parseInt(select.value), bookId);
            select.value = ''; // Reset the select after adding
        } catch (e) {
            console.error('Failed to add book to list:', e);
        }
    }

    function handleSelectBinding(node: HTMLSelectElement, bookId: number) {
        selectElements.set(bookId, node);
        return {
            destroy() {
                selectElements.delete(bookId);
            }
        };
    }

    // Initialize data on mount
    onMount(async () => {
        await initializeStores();
    });
</script>

<div class="book-list unlisted-books">
    <div class="container">
        <h2>Unlisted Books</h2>
        <div class="books-grid">
            {#if $unlistedBooks.length === 0}
                <p class="empty">No unlisted books</p>
            {/if}
            {#each $unlistedBooks as book (book.id)}
                <div class="book-card">
                    <div class="book-content">
                        {#if editingId === book.id}
                            <div class="edit-form">
                                <button 
                                    class="edit-button"
                                    on:click={cancelEdit}
                                    title="Cancel"
                                >
                                    ✕
                                </button>
                                <label>
                                    Title:
                                    <input 
                                        type="text" 
                                        bind:value={editTitle}
                                        placeholder="Title"
                                    />
                                </label>
                                <label>
                                    Author:
                                    <input 
                                        type="text" 
                                        bind:value={editAuthor}
                                        placeholder="Author"
                                    />
                                </label>
                                <label>
                                    Description:
                                    <textarea 
                                        bind:value={editDescription}
                                        placeholder="Description"
                                    ></textarea>
                                </label>
                                <div class="edit-actions">
                                    <button 
                                        class="save-button"
                                        on:click={saveEdit}
                                    >
                                        Save
                                    </button>
                                </div>
                            </div>
                        {:else}
                            <table class="action-buttons">
                                <tbody>
                                    <tr>
                                        <td>
                                            <button 
                                                class="edit-button"
                                                on:click={() => startEdit(book)}
                                                title="Edit"
                                            >
                                                ✏️
                                            </button>
                                        </td>
                                        <td>
                                            <button 
                                                class="delete-button"
                                                on:click={() => handleDelete(book)}
                                                title="Delete"
                                            >
                                                🗑️
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <h3>{book.title}</h3>
                            <p class="author">by {book.author}</p>
                            {#if book.description}
                                <p class="description">{book.description}</p>
                            {/if}
                        {/if}
                    </div>
                    <div class="add-to-list">
                        <select 
                            use:handleSelectBinding={book.id}
                            value=""
                        >
                            <option value="" disabled>Select a list...</option>
                            {#each $lists as list}
                                <option value={list.id}>{list.name}</option>
                            {/each}
                        </select>
                        <button 
                            class="add-button"
                            on:click={() => addToList(book.id)}
                        >
                            Add to List
                        </button>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>
