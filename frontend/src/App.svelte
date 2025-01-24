<script lang="ts">
  import { onMount } from 'svelte';
  import { lists, initializeStores, createList } from './lib/stores';
  import BookList from './lib/BookList.svelte';
  import AddBookForm from './lib/AddBookForm.svelte';
  import UnlistedBooks from './lib/UnlistedBooks.svelte';
  import './styles/main.scss';

  let newListName = '';
  let error = '';

  onMount(async () => {
    try {
      await initializeStores();
    } catch (e) {
      error = 'Failed to load data';
    }
  });

  async function handleCreateList() {
    if (!newListName) {
      error = 'List name is required';
      return;
    }

    try {
      await createList(newListName);
      newListName = '';
      error = '';
    } catch (e) {
      error = 'Failed to create list';
    }
  }
</script>

<main>
  <h1>Book Tracker</h1>

  <div class="content">
    <div class="lists-section">
      <div class="lists-container">
        <div class="add-list">
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
            <button on:click={handleCreateList}>Create List</button>
          </div>
        </div>

        <UnlistedBooks />

        {#each $lists as list (list.id)}
          <BookList {list} />
        {/each}
      </div>
    </div>

    <div class="sidebar">
      <AddBookForm />
    </div>
  </div>
</main>

<style lang="scss">
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    text-align: center;
    margin-bottom: 2rem;
    color: #2c3e50;
  }

  .content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }

  .lists-section {
    min-width: 0; // Prevent flex item from overflowing
  }

  .sidebar {
    min-width: 0; // Prevent flex item from overflowing
  }

  .error {
    color: #e74c3c;
    margin-bottom: 1rem;
  }
</style>
