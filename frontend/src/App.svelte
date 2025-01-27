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
  let showSidebar = false;

  // Subscribe to lists store changes
  $: allLists = $lists;

  onMount(() => {
    initializeStores().catch(e => {
      error = 'Failed to load data';
    });

    return () => {
      document.body.classList.remove('sidebar-open');
    };
  });

  function toggleSidebar() {
    showSidebar = !showSidebar;
    document.body.classList.toggle('sidebar-open', showSidebar);
  }

  function handleMainContentClick() {
    if (showSidebar) {
      showSidebar = false;
      document.body.classList.remove('sidebar-open');
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Escape' && showSidebar) {
      showSidebar = false;
      document.body.classList.remove('sidebar-open');
    }
  }
</script>

<div class="app-container">
  <h1>Book Tracker</h1>

  <button 
    class="menu-button" 
    on:click={toggleSidebar}
    aria-label={showSidebar ? 'Close menu' : 'Open menu'}
    aria-expanded={showSidebar}
  >
    {showSidebar ? '✕' : '☰'}
  </button>

  <div class="content">
    <div 
      class="left-sidebar"
      class:open={showSidebar}
      role="navigation"
      aria-label="Main menu"
    >
      <ListsSidebar />
    </div>

    <button 
      type="button"
      class="main-content-overlay"
      on:click={handleMainContentClick}
      on:keydown={handleKeyDown}
      aria-label="Close menu overlay"
      tabindex="-1"
      style="display: {showSidebar ? 'block' : 'none'}"
    ></button>

    <main class="main-content">
      {#if error}
        <div class="error">{error}</div>
      {/if}
      
      <div class="lists-container">
        {#each allLists as list (list.id)}
          <BookList {list} />
        {/each}
      </div>
    </main>

    <aside class="right-sidebar">
      <AddBookForm />
      <UnlistedBooks />
    </aside>
  </div>
</div>

<svelte:head>
  {#if showSidebar}
    <style>
      body {
        overflow: hidden;
      }
    </style>
  {/if}
</svelte:head>
