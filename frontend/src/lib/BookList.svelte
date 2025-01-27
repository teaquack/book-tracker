<script lang="ts">
    import { lists, books, addBookToList, booksInList, updateBook, deleteBook } from './stores';
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
    let error = '';

    function startEdit(book: BookWithSelect) {
        editingId = book.id;
        editTitle = book.title;
        editAuthor = book.author;
        editDescription = book.description || '';
        error = '';
    }

    function cancelEdit() {
        editingId = null;
        error = '';
    }

    async function saveEdit() {
        if (editingId === null) return;

        try {
            error = '';
            await updateBook(editingId, {
                title: editTitle,
                author: editAuthor,
                description: editDescription
            });
            editingId = null;
        } catch (e) {
            error = 'Failed to update book. Please try again.';
            console.error('Failed to update book:', e);
        }
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
            error = '';
            await addBookToList(targetListId, bookId);
            select.value = ''; // Reset the select after moving
        } catch (e) {
            error = 'Failed to move book to list. Please try again.';
            console.error('Failed to move book to list:', e);
        }
    }

    async function handleDelete(book: BookWithSelect) {
        try {
            error = '';
            // Update the book to remove its list_id
            await updateBook(book.id, {
                list_id: undefined
            }, true);
        } catch (e) {
            error = 'Failed to remove book from list. Please try again.';
            console.error('Failed to remove book from list:', e);
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
    <div class="container">
        <h2>{list.name}</h2>
        {#if error}
            <div class="error">{error}</div>
        {/if}
        <div class="books-grid">
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
                                        Title
                                        <input 
                                            type="text" 
                                            bind:value={editTitle}
                                            placeholder="Enter title"
                                        />
                                    </label>
                                    <label>
                                        Author
                                        <input 
                                            type="text" 
                                            bind:value={editAuthor}
                                            placeholder="Enter author"
                                        />
                                    </label>
                                    <label>
                                        Description
                                        <textarea 
                                            bind:value={editDescription}
                                            placeholder="Enter description"
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
</div>
