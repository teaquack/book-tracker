<script lang="ts">
    import { tags, createTag, deleteTag } from './stores/index';
    import type { Tag } from './types';

    let newTagName = '';
    let error = '';
    let allTags: Tag[] = [];

    // Subscribe to tags store changes
    $: allTags = $tags;

    async function handleCreateTag() {
        if (!newTagName.trim()) {
            error = 'Tag name is required';
            return;
        }

        try {
            error = '';
            await createTag(newTagName.trim());
            newTagName = '';
        } catch (e) {
            error = 'Failed to create tag';
            console.error('Error creating tag:', e);
        }
    }

    async function handleDeleteTag(tagId: number) {
        if (!confirm('Are you sure you want to delete this tag?')) {
            return;
        }

        try {
            error = '';
            await deleteTag(tagId);
        } catch (e) {
            error = 'Failed to delete tag';
            console.error('Error deleting tag:', e);
        }
    }
</script>

<div class="tags-panel">
    <section class="create-tag">
        <h2>Create New Tag</h2>
        {#if error}
            <div class="error">{error}</div>
        {/if}

        <div class="input-group">
            <input
                type="text"
                bind:value={newTagName}
                placeholder="Enter tag name"
            />
        </div>
        <button class="create-button" on:click={handleCreateTag}>Create Tag</button>
    </section>

    <section class="all-tags">
        {#if allTags.length === 0}
            <p class="empty">No tags yet</p>
        {:else}
            <ul>
                {#each allTags as tag (tag.id)}
                    <li class="tag-item">
                        <div class="tag-info">
                            <span class="tag-name">{tag.name}</span>
                        </div>
                        <button
                            class="delete-button"
                            on:click={() => handleDeleteTag(tag.id)}
                            title="Delete tag"
                            aria-label="Delete tag {tag.name}"
                        >
                            ×
                        </button>
                    </li>
                {/each}
            </ul>
        {/if}
    </section>
</div>
