<script lang="ts">
import { lists, createList, books, deleteList } from './stores/index';

let newListName = '';
let error = '';
let allLists: typeof $lists = [];

// Subscribe to lists store changes
$: allLists = $lists;

async function handleCreateList() {
  if (!newListName.trim()) {
    error = 'List name is required';
    return;
  }

  try {
    await createList(newListName);
    newListName = '';
    error = '';
  } catch (e) {
    error = 'Failed to create list';
    console.error('Error creating list:', e);
  }
}

async function handleDeleteList(listId: number) {
  if (!confirm('Are you sure you want to delete this list? Books in this list will be moved to Unlisted Books.')) {
    return;
  }

  try {
    await deleteList(listId);
  } catch (e) {
    error = 'Failed to delete list';
    console.error('Error deleting list:', e);
  }
}

function getBookCount(listId: number): number {
  return $books.filter(book => book.list_id === listId).length;
}
</script>

<div class="lists-sidebar">
  <section class="create-list">
    <h2>Create New List</h2>
    {#if error}
      <div class="error">{error}</div>
    {/if}
    <div class="input-group">
      <input
        type="text"
        bind:value={newListName}
        placeholder="Enter list name"
      />
    </div>
    <button class="create-button" on:click={handleCreateList}>Create List</button>
  </section>

  <section class="all-lists">
    <h2>Your Lists</h2>
    <ul>
      {#each allLists as list (list.id)}
        <li class="list-item">
          <div class="list-info">
            <span class="list-name">{list.name}</span>
            <span class="book-count">{getBookCount(list.id)}</span>
          </div>
          <button 
            class="delete-button" 
            on:click={() => handleDeleteList(list.id)}
            title="Delete list"
          >
            ×
          </button>
        </li>
      {/each}
    </ul>
  </section>
</div>
