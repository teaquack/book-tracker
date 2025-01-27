<script lang="ts">
  import { onMount } from 'svelte';
  import { lists, initializeStores } from './lib/stores/index';
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
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleMainContentClick();
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

    <div 
      class="main-content" 
      on:click={handleMainContentClick}
      on:keydown={handleKeyDown}
      role="button"
      tabindex="0"
    >
      {#if error}
        <div class="error">{error}</div>
      {/if}
      
      <div class="lists-container">
        <UnlistedBooks />
        {#each allLists as list (list.id)}
          <BookList {list} />
        {/each}
      </div>
    </div>

    <div class="right-sidebar">
      <AddBookForm />
    </div>
  </div>
</div>
