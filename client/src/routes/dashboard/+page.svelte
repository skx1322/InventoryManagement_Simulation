<script lang="ts">
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

<main class="flex-1 p-10 lg:p-16 overflow-y-auto">
  <header class="flex justify-between items-end mb-12">
    <div>
      <h2 class="text-4xl font-extrabold text-gray-900 tracking-tight">
        {data.user?.organization_name}
      </h2>
      <p class="text-xl text-gray-500 mt-2">
        System Status: <span class="text-green-600 font-medium"
          >Precise Inventory Active</span
        >
      </p>
    </div>
    <div class="w-1/3 max-w-md">
      <div class="relative">
        <input
          type="text"
          placeholder="Search global inventory..."
          class="w-full pl-12 pr-4 py-4 bg-white border border-gray-200 rounded-xl text-xl shadow-sm outline-none focus:ring-2 focus:ring-[#4A607C] transition-all"
        />
        <span class="absolute left-4 top-4.5 text-gray-400 text-xl">🔍</span>
      </div>
    </div>
  </header>

  <div class="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-12">
    <div
      class="bg-white p-10 rounded-2xl shadow-sm border-l-8 border-blue-500 flex flex-col justify-center"
    >
      <p class="text-sm font-bold text-gray-400 uppercase tracking-widest">
        Total Items
      </p>
      <p class="text-4xl font-black text-gray-800 mt-2">
        {data.totalItems.toLocaleString()}
      </p>
    </div>
    <div
      class="bg-[#4A607C] p-10 rounded-2xl shadow-lg text-white flex flex-col justify-center"
    >
      <p class="text-sm font-bold text-gray-300 uppercase tracking-widest">
        Inventory Value
      </p>
      <p class="text-4xl font-black mt-2">
        ${data.totalValue.toLocaleString()}
      </p>
    </div>
    <div
      class="bg-white p-10 rounded-2xl shadow-sm border-l-8 border-orange-400 flex flex-col justify-center"
    >
      <p class="text-sm font-bold text-gray-400 uppercase tracking-widest">
        Stock Alerts
      </p>
      <p class="text-4xl font-black text-gray-800 mt-2">
        {data.product?.filter((p) => p.quantity < 10).length ?? 0}
      </p>
    </div>
  </div>

  <section
    class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-12"
  >
    <div class="p-8 border-b border-gray-100 flex justify-between items-center">
      <h3 class="text-2xl font-bold text-gray-800">Live Inventory Feed</h3>
      <button
        class="px-6 py-2 bg-gray-50 rounded-lg text-sm font-bold text-[#4A607C] uppercase tracking-wider hover:bg-gray-100 transition-all"
        >Export Report</button
      >
    </div>
    <table class="w-full text-left">
      <thead>
        <tr
          class="bg-gray-50/50 text-sm font-bold text-gray-400 uppercase tracking-widest"
        >
          <th class="p-6">Product Information</th>
          <th class="p-6">Serial SKU</th>
          <th class="p-6 text-center">Status</th>
          <th class="p-6">Unit Price</th>
          <th class="p-6 text-right">System Timestamp</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-50">
        {#each data.product ?? [] as item}
          <tr class="hover:bg-blue-50/30 transition-colors group">
            <td class="p-6 flex items-center gap-6">
              <img
                src={data.img_url + "/" + item.product_image}
                alt={item.product_name}
                class="w-16 h-16 rounded-xl bg-gray-100 object-cover shadow-sm group-hover:scale-105 transition-transform"
              />
              <span class="text-2xl font-bold text-gray-700"
                >{item.product_name}</span
              >
            </td>
            <td class="p-6 text-lg font-mono text-gray-400"
              >{item.product_sku}</td
            >
            <td class="p-6 text-center">
              <span
                class="px-4 py-2 text-nowrap rounded-lg text-sm font-black uppercase tracking-tighter {item.quantity <
                10
                  ? 'bg-red-100 text-red-700'
                  : 'bg-green-100 text-green-700'}"
              >
                {item.quantity} Units
              </span>
            </td>
            <td class="p-6 text-2xl font-medium text-gray-600">${item.price}</td
            >
            <td class="p-6 text-right text-lg text-gray-400"
              >{item.updated_at}</td
            >
          </tr>
        {/each}
      </tbody>
    </table>
  </section>

  <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
    {#each [{ icon: "📷", label: "Scan Item" }, { icon: "📋", label: "Generate Barcode" }, { icon: "➕", label: "Add Product" }, { icon: "📤", label: "Export CSV" }] as action}
      <button
        class="flex items-center gap-6 p-8 bg-white border-2 border-dashed border-gray-200 rounded-2xl hover:border-[#4A607C] hover:bg-blue-50/20 transition-all group"
      >
        <span class="text-4xl group-hover:rotate-12 transition-transform"
          >{action.icon}</span
        >
        <span class="text-xl font-bold uppercase tracking-tight text-gray-700"
          >{action.label}</span
        >
      </button>
    {/each}
  </div>
</main>
