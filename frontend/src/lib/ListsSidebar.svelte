<script lang="ts">
import { lists, createList, books, deleteList } from './stores';

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

<style lang="scss">
  .lists-sidebar {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    height: 100%;

    section {
      h2 {
        font-size: 1.25rem;
        margin-bottom: 1rem;
        color: #2c3e50;
      }
    }
  }

  .create-list {
    .input-group {
      margin-bottom: 1rem;

      input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 0.9rem;

        &::placeholder {
          color: #a0aec0;
        }

        &:focus {
          outline: none;
          border-color: #3498db;
          box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }
      }
    }

    .create-button {
      width: 100%;
      padding: 0.5rem;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.9rem;
      transition: background-color 0.2s ease;

      &:hover {
        background: #2980b9;
      }
    }
  }

  .error {
    color: #e74c3c;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }

  .all-lists {
    flex: 1;
    overflow-y: auto;

    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .list-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem;
      background: white;
      border-radius: 4px;
      border: 1px solid #ddd;
      transition: border-color 0.2s ease;

      &:hover {
        border-color: #3498db;

        .delete-button {
          opacity: 1;
        }
      }

      .list-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex: 1;
        min-width: 0;
      }

      .list-name {
        font-weight: 500;
        color: #2c3e50;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .book-count {
        background: #edf2f7;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        color: #4a5568;
        flex-shrink: 0;
      }

      .delete-button {
        background: none;
        border: none;
        color: #e53e3e;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        margin: -0.25rem -0.5rem;
        opacity: 0;
        transition: all 0.2s ease;
        border-radius: 4px;

        &:hover {
          background: #fed7d7;
        }
      }
    }
  }
</style>
