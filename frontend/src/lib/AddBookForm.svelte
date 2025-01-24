<script lang="ts">
    import { createBook, lists } from './stores';
    
    let title = '';
    let author = '';
    let description = '';
    let selectedListId = '';
    let error = '';

    async function handleSubmit() {
        try {
            error = '';
            await createBook(
                { title, author, description },
                selectedListId ? parseInt(selectedListId) : undefined
            );
            
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

<style lang="scss">
    .add-book-form {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

        h2 {
            margin: 0 0 1.5rem 0;
            color: #2c3e50;
        }
    }

    .form-group {
        margin-bottom: 1rem;

        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #4a5568;
        }

        input, textarea, select {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            font-size: 1rem;

            &:focus {
                outline: none;
                border-color: #4299e1;
                box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
            }
        }
    }

    .error {
        color: #e74c3c;
        background: #fed7d7;
        padding: 0.5rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }

    button {
        width: 100%;
        padding: 0.75rem;
        background: #4299e1;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;

        &:hover {
            background: #3182ce;
        }
    }
</style>
