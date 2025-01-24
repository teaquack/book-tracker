<script lang="ts">
  import ListsSidebar from './lib/ListsSidebar.svelte';
  import BookList from './lib/BookList.svelte';
  import UnlistedBooks from './lib/UnlistedBooks.svelte';
  import AddBookForm from './lib/AddBookForm.svelte';
  import { lists } from './lib/stores';
  import { onMount } from 'svelte';

  let showSidebar = false;

  function toggleSidebar() {
    showSidebar = !showSidebar;
    document.body.classList.toggle('sidebar-open', showSidebar);
  }

  // Close sidebar when clicking outside on mobile
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

  onMount(() => {
    return () => {
      document.body.classList.remove('sidebar-open');
    };
  });
</script>

<div class="app-container">
  <h1>Book Tracker</h1>

  <div class="content">
    <button 
      class="menu-button" 
      on:click={toggleSidebar}
      aria-label={showSidebar ? 'Close menu' : 'Open menu'}
      aria-expanded={showSidebar}
    >
      {showSidebar ? '✕' : '☰'}
    </button>

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
      <div class="lists-container">
        <UnlistedBooks />
        {#each $lists as list (list.id)}
          <BookList {list} />
        {/each}
      </div>
    </main>

    <aside class="right-sidebar">
      <AddBookForm />
    </aside>
  </div>
</div>
