<script lang="ts">
	let { children } = $props();
</script>

<header class="absolute top-0 w-full flex justify-between items-center p-6 px-10">
  <div class="text-xl font-bold text-gray-800 tracking-tight">Monolith Inventory</div>
  <div class="flex items-center gap-6 text-gray-500">
    <button class="hover:text-gray-800">
      <span class="sr-only">Help</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    </button>
    <button class="hover:text-gray-800">
      <span class="sr-only">Toggle Theme</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
    </button>
  </div>
</header>

{@render children()}
