<script lang="ts">
	let { children } = $props();
</script>

<div class="flex min-h-screen w-full bg-[#F8FAFC]">
    <aside class="w-64 lg:w-72 bg-white border-r border-gray-200 flex flex-col sticky top-0 h-screen">
        <div class="p-8">
            <h1 class="text-2xl font-bold text-gray-800 tracking-tight">Monolith</h1>
            <p class="text-sm text-gray-400 font-bold uppercase tracking-widest">Inventory Systems</p>
        </div>

        <nav class="flex-1 px-6 space-y-4">
            <a href="/dashboard" class="flex items-center gap-4 p-4 bg-[#4A607C] text-white rounded-lg shadow-sm transition-all text-xl">
                <span>📊</span> Dashboard
            </a>
            <button class="w-full flex items-center gap-4 p-4 text-gray-500 hover:bg-gray-50 rounded-lg transition-colors text-xl">
                <span>📦</span> Inventory
            </button>
            <button class="w-full flex items-center gap-4 p-4 text-gray-500 hover:bg-gray-50 rounded-lg transition-colors text-xl">
                <span>⚙️</span> Settings
            </button>
        </nav>

        <div class="p-6 border-t border-gray-100 bg-gray-50">
            <!-- <div class="flex items-center gap-4">
                <img 
                    src={data.img_url + '/' + data.user?.user_avatar}
                    alt="User" 
                    class="w-14 h-14 rounded-full border-2 border-white shadow-sm object-cover"
                />
                <div class="overflow-hidden">
                    <p class="text-sm font-bold text-gray-800 truncate">{data.user?.username}</p>
                    <p class="text-xs text-gray-500 truncate">{data.user?.email}</p>
                </div>
            </div> -->
            <button class="mt-6 w-full text-sm font-bold text-red-500 uppercase tracking-widest hover:bg-red-50 p-3 rounded-lg border border-transparent hover:border-red-100 transition-all">
                Logout
            </button>
        </div>
    </aside>

    {@render children()}

</div>
