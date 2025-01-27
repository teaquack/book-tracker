<script lang="ts">
    import { createBook, lists } from './stores/index';
    
    let title = '';
    let author = '';
    let description = '';
    let selectedListId = '';
    let error = '';

    async function handleSubmit() {
        try {
            error = '';
            await createBook({
                title,
                author,
                description,
                list_id: selectedListId ? parseInt(selectedListId) : undefined
            });
            
            // Reset form
            title = '';
            author = '';
            description = '';
            selectedListId = '';
        } catch (e) {
            error = 'Failed to add book. Please try again.';
            console.error('Failed to add book:', e);
        }
    }
</script>

<form class="add-book-form" on:submit|preventDefault={handleSubmit}>
    <h2>Add New Book</h2>
    
    {#if error}
        <div class="error">{error}</div>
    {/if}

    <div class="form-group">
        <label for="title">Title</label>
        <input
            id="title"
            bind:value={title}
            required
        />
    </div>

    <div class="form-group">
        <label for="author">Author</label>
        <input
            id="author"
            bind:value={author}
            required
        />
    </div>

    <div class="form-group">
        <label for="description">Description (optional)</label>
        <textarea
            id="description"
            bind:value={description}
            rows="3"
        ></textarea>
    </div>

    <div class="form-group">
        <label for="list">Add to List (optional)</label>
        <select
            id="list"
            bind:value={selectedListId}
        >
            <option value="">No List</option>
            {#each $lists as list}
                <option value={list.id}>{list.name}</option>
            {/each}
        </select>
    </div>

    <button type="submit">Add Book</button>
</form>
