<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	let { children } = $props();

	import "../app.css"
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}

<footer
  class="fixed bottom-4 w-full flex justify-between px-10 text-base text-gray-400 uppercase tracking-tighter"
>
  <div>© {new Date().getFullYear()} Sin's Inventory Management Simulator. For the fun.</div>
  <div class="space-x-4">
    <a href="/">Privacy Policy</a>
    <a href="/">Terms of Service</a>
    <a href="/">Security</a>
  </div>
</footer>
