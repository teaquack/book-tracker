<script lang="ts">
  import { onMount } from 'svelte';
  import { lists, initializeStores } from './lib/stores';
  import BookList from './lib/BookList.svelte';
  import AddBookForm from './lib/AddBookForm.svelte';
  import UnlistedBooks from './lib/UnlistedBooks.svelte';
  import ListsSidebar from './lib/ListsSidebar.svelte';
  import './styles/main.scss';

  let error = '';
  let allLists: typeof $lists = [];
  let isSidebarOpen = false;

  // Subscribe to lists store changes
  $: allLists = $lists;

  onMount(async () => {
    try {
      await initializeStores();
    } catch (e) {
      error = 'Failed to load data';
    }
  });

  function toggleSidebar() {
    isSidebarOpen = !isSidebarOpen;
  }
</script>

<main>
  <h1>Book Tracker</h1>

  <div class="content">
    <!-- Mobile Menu Button -->
    <button class="menu-button" on:click={toggleSidebar}>
      {#if isSidebarOpen}
        ✕
      {:else}
        ☰
      {/if}
    </button>

    <!-- Left Sidebar -->
    <div class="left-sidebar" class:open={isSidebarOpen}>
      <ListsSidebar />
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="lists-container">
        <UnlistedBooks />
        {#each allLists as list (list.id)}
          <BookList {list} />
        {/each}
      </div>
    </div>

    <!-- Right Sidebar -->
    <div class="right-sidebar">
      <AddBookForm />
    </div>
  </div>
</main>

<style lang="scss">
  main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    text-align: center;
    margin-bottom: 2rem;
    color: #2c3e50;
  }

  .menu-button {
    display: none;
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 1000;
    padding: 0.5rem;
    font-size: 1.5rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    @media (max-width: 1024px) {
      display: block;
    }
  }

  .content {
    display: grid;
    grid-template-columns: 250px 1fr 300px;
    gap: 2rem;
    position: relative;
    min-height: calc(100vh - 150px);
  }

  .left-sidebar {
    background: #f8f9fa;
    border-radius: 8px;
    height: 100%;
    overflow-y: auto;

    @media (max-width: 1024px) {
      position: fixed;
      top: 0;
      left: -250px;
      bottom: 0;
      width: 250px;
      z-index: 100;
      transition: transform 0.3s ease;
      box-shadow: none;

      &.open {
        transform: translateX(250px);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      }
    }
  }

  .main-content {
    min-width: 0;
  }

  .lists-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .right-sidebar {
    @media (max-width: 1200px) {
      display: none;
    }
  }

  /* Overlay for mobile sidebar */
  :global(body) {
    &::after {
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
      z-index: 90;
    }

    &.sidebar-open {
      &::after {
        opacity: 1;
        visibility: visible;
      }
    }
  }
</style>

<svelte:head>
  {#if isSidebarOpen}
    <style>
      body {
        overflow: hidden;
      }
    </style>
  {/if}
</svelte:head>
