<script lang="ts">
    import type { PageProps } from "./$types";

    let { data }: PageProps = $props();
</script>

<div class="flex min-h-screen bg-[#F8FAFC]">
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div class="p-6">
            <h1 class="text-xl font-bold text-gray-800 tracking-tight">Monolith</h1>
            <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Inventory Systems</p>
        </div>

        <nav class="flex-1 px-4 space-y-2">
            <a href="/dashboard" class="flex items-center gap-3 p-3 bg-[#4A607C] text-white rounded-md">
                <span class="text-lg">📊</span> Dashboard
            </a>
            <button class="w-full flex items-center gap-3 p-3 text-gray-500 hover:bg-gray-50 rounded-md transition-colors">
                <span class="text-lg">📦</span> Inventory
            </button>
            <button class="w-full flex items-center gap-3 p-3 text-gray-500 hover:bg-gray-50 rounded-md transition-colors">
                <span class="text-lg">⚙️</span> Settings
            </button>
        </nav>

        <div class="p-4 border-t border-gray-100 bg-gray-50">
            <div class="flex items-center gap-3">
                <img 
                    src={data.img_url + '/' + data.user?.user_avatar}
                    alt="User" 
                    class="w-10 h-10 rounded-full border border-gray-300 object-cover"
                />
                <div class="overflow-hidden">
                    <p class="text-xs font-bold text-gray-800 truncate">{data.user?.username}</p>
                    <p class="text-[10px] text-gray-500 truncate">{data.user?.email}</p>
                </div>
            </div>
            <button class="mt-4 w-full text-[10px] font-bold text-red-500 uppercase tracking-widest hover:bg-red-50 p-2 rounded transition-colors">
                Logout
            </button>
        </div>
    </aside>

    <main class="flex-1 p-8 overflow-y-auto">
        <header class="flex justify-between items-center mb-8">
            <div>
                <h2 class="text-2xl font-bold text-gray-800">{data.user?.organization_name}</h2>
                <p class="text-sm text-gray-500">System Status: Precise Inventory Active</p>
            </div>
            <div class="flex gap-4">
                <div class="relative">
                    <input type="text" placeholder="Search inventory..." class="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-md text-sm outline-none focus:ring-2 focus:ring-[#4A607C]" />
                    <span class="absolute left-3 top-2.5 text-gray-400 text-xs">🔍</span>
                </div>
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white p-6 rounded-lg shadow-sm border-l-4 border-blue-500">
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Total Items</p>
                <p class="text-3xl font-bold text-gray-800 mt-1">{data.totalItems.toLocaleString()}</p>
            </div>
            <div class="bg-[#4A607C] p-6 rounded-lg shadow-sm text-white">
                <p class="text-[10px] font-bold text-gray-300 uppercase tracking-widest">Inventory Value</p>
                <p class="text-3xl font-bold mt-1">${data.totalValue.toLocaleString()}</p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border-l-4 border-orange-400">
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Stock Alerts</p>
                <p class="text-3xl font-bold text-gray-800 mt-1">{data.product?.filter(p => p.quantity < 10).length ?? 0}</p>
            </div>
        </div>

        <section class="bg-white rounded-lg shadow-sm overflow-hidden mb-8">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center">
                <h3 class="font-bold text-gray-800">Recent Stock</h3>
                <button class="text-xs font-bold text-[#4A607C] uppercase hover:underline">View All</button>
            </div>
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-50 text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                        <th class="p-4">Product</th>
                        <th class="p-4">SKU</th>
                        <th class="p-4 text-center">Quantity</th>
                        <th class="p-4">Price</th>
                        <th class="p-4 text-right">Last Update</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    {#each data.product ?? [] as item}
                        <tr class="hover:bg-gray-50 transition-colors">
                            <td class="p-4 flex items-center gap-3">
                                <img src={data.img_url + '/' + item.product_image} alt={item.product_name} class="w-8 h-8 rounded bg-gray-100 object-cover" />
                                <span class="text-sm font-medium text-gray-700">{item.product_name}</span>
                            </td>
                            <td class="p-4 text-xs font-mono text-gray-400">{item.product_sku}</td>
                            <td class="p-4 text-center">
                                <span class="px-2 py-1 rounded-full text-xs font-bold {item.quantity < 10 ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}">
                                    {item.quantity} Units
                                </span>
                            </td>
                            <td class="p-4 text-sm text-gray-600">${item.price}</td>
                            <td class="p-4 text-right text-[10px] text-gray-400">{item.updated_at}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </section>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button onclick={() => {}} class="flex flex-col items-center justify-center p-6 bg-white border border-dashed border-gray-300 rounded-lg hover:border-[#4A607C] hover:text-[#4A607C] transition-all group">
                <span class="text-2xl mb-2 group-hover:scale-110 transition-transform">📷</span>
                <span class="text-[10px] font-bold uppercase">Scan Item</span>
            </button>
            <button onclick={() => {}} class="flex flex-col items-center justify-center p-6 bg-white border border-dashed border-gray-300 rounded-lg hover:border-[#4A607C] hover:text-[#4A607C] transition-all group">
                <span class="text-2xl mb-2 group-hover:scale-110 transition-transform">📋</span>
                <span class="text-[10px] font-bold uppercase">Generate Barcode</span>
            </button>
            <button class="flex flex-col items-center justify-center p-6 bg-white border border-dashed border-gray-300 rounded-lg hover:border-[#4A607C] hover:text-[#4A607C] transition-all group">
                <span class="text-2xl mb-2 group-hover:scale-110 transition-transform">➕</span>
                <span class="text-[10px] font-bold uppercase">Add Product</span>
            </button>
            <button onclick={() => {}} class="flex flex-col items-center justify-center p-6 bg-white border border-dashed border-gray-300 rounded-lg hover:border-[#4A607C] hover:text-[#4A607C] transition-all group">
                <span class="text-2xl mb-2 group-hover:scale-110 transition-transform">📤</span>
                <span class="text-[10px] font-bold uppercase">Export CSV</span>
            </button>
        </div>
    </main>
</div>
