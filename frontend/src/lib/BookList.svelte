<script lang="ts">
    import { lists, addBookToList, booksInList, updateBook, deleteBook } from './stores';
    import type { BookList, Book } from './stores';

    export let list: BookList;

    type BookWithSelect = {
        id: number;
        title: string;
        author: string;
        description?: string;
        list_id?: number;
        selectElement?: HTMLSelectElement;
    };

    // Simple editing state
    let editingId: number | null = null;
    let editTitle = '';
    let editAuthor = '';
    let editDescription = '';

    function startEdit(book: BookWithSelect) {
        editingId = book.id;
        editTitle = book.title;
        editAuthor = book.author;
        editDescription = book.description || '';
    }

    function cancelEdit() {
        editingId = null;
    }

    async function moveToList(bookId: number, select: HTMLSelectElement) {
        if (!select.value) return;
        const targetListId = parseInt(select.value);
        
        // Don't do anything if moving to the same list
        if (targetListId === list.id) {
            select.value = '';
            return;
        }

        try {
            await addBookToList(targetListId, bookId);
            select.value = ''; // Reset the select after moving
        } catch (e) {
            console.error('Failed to move book to list:', e);
        }
    }

    async function saveEdit() {
        if (editingId === null) return;

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

    async function handleDelete(book: BookWithSelect) {
        if (!confirm(`Are you sure you want to delete "${book.title}"?`)) {
            return;
        }

        try {
            await deleteBook(book.id);
        } catch (e) {
            console.error('Failed to delete book:', e);
        }
    }

    // Get the derived store for this list's books
    const listBooksStore = booksInList(list.id);
    
    // Get other lists for the move options, but only when lists changes
    let otherLists: BookList[] = [];
    $: {
        if ($lists) {
            otherLists = $lists.filter(l => l.id !== list.id);
        }
    }

    // Cast books to include selectElement, but only when books change
    let booksWithSelect: BookWithSelect[] = [];
    $: {
        if ($listBooksStore) {
            booksWithSelect = $listBooksStore.map(book => ({
                ...book,
                selectElement: undefined
            }));
        }
    }
</script>

<div class="book-list">
    <h2>{list.name}</h2>
    <div class="books">
        {#if booksWithSelect.length === 0}
            <p class="empty">No books in this list</p>
        {:else}
            {#each booksWithSelect as book (book.id)}
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
                            <div class="action-buttons">
                                <button 
                                    class="edit-button"
                                    on:click={() => startEdit(book)}
                                    title="Edit"
                                >
                                    ✏️
                                </button>
                                <button 
                                    class="delete-button"
                                    on:click={() => handleDelete(book)}
                                    title="Delete"
                                >
                                    🗑️
                                </button>
                            </div>
                            <h3>{book.title}</h3>
                            <p class="author">by {book.author}</p>
                            {#if book.description}
                                <p class="description">{book.description}</p>
                            {/if}
                        {/if}
                    </div>
                    {#if otherLists.length > 0}
                        <div class="move-to-list">
                            <select 
                                bind:this={book.selectElement}
                                value=""
                            >
                                <option value="" disabled>Move to list...</option>
                                {#each otherLists as otherList}
                                    <option value={otherList.id}>{otherList.name}</option>
                                {/each}
                            </select>
                            <button 
                                class="move-button"
                                on:click={() => book.selectElement && moveToList(book.id, book.selectElement)}
                            >
                                Move
                            </button>
                        </div>
                    {/if}
                </div>
            {/each}
        {/if}
    </div>
</div>
