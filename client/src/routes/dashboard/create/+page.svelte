<script lang="ts">
  import { enhance } from "$app/forms";
  import warehouseImg from "$lib/assets/working.png";

  let stockLevel = $state(150);
</script>

<main class="min-h-screen bg-gray-100/50 flex items-center justify-center p-8 grow">
  <div class="w-full bg-white rounded-xl shadow-2xl overflow-hidden">
    <div
      class="px-10 py-6 border-b border-gray-100 flex justify-between items-center bg-white"
    >
      <div>
        <h1 class="text-3xl font-bold text-gray-800">Create New Product</h1>
        <p class="text-gray-400 text-lg">
          Register a new asset into the StockMaster monolith.
        </p>
      </div>
      <div class="flex gap-4">
        <a
          href="/dashboard"
          class="px-6 py-2 text-gray-400 font-bold hover:text-gray-600 transition-colors"
          >Cancel</a
        >
        <button
          form="product-form"
          type="submit"
          class="bg-[#4A607C] text-white px-8 py-2 rounded shadow-lg font-bold hover:bg-[#3d4f66] transition-all"
        >
          Save Product
        </button>
      </div>
    </div>

    <form
      id="product-form"
      method="POST"
      action="?/create"
      use:enhance
      enctype="multipart/form-data"
      class="flex flex-col md:flex-row"
    >
      <section class="md:w-1/3 bg-[#F8FAFC] p-10 flex flex-col gap-6">
        <div>
          <span
            class="inline-block bg-[#D1D9E2] text-[#4A607C] text-lg font-bold px-2 py-1 rounded mb-4 uppercase tracking-widest"
            >System Entry</span
          >
          <h2 class="text-2xl font-bold text-gray-800">Precision Control</h2>
          <p class="text-lg text-gray-500 leading-relaxed mt-2">
            Ensure all fields are audited. SKU generation follows the Monolith
            protocol for cross-regional tracking.
          </p>
        </div>
        <div class="mt-auto">
          <img
            src={warehouseImg}
            alt="Monolith Warehouse"
            class="rounded-lg shadow-md opacity-80 object-cover aspect-square"
          />
        </div>
      </section>

      <section class="md:w-2/3 p-10 space-y-8">
        <div class="grid grid-cols-2 gap-8">
          <div class="space-y-2">
            <label
              for="product_name"
              class="block text-lg font-bold text-gray-400 uppercase tracking-widest"
              >Product Name</label
            >
            <input
              type="text"
              id="product_name"
              name="product_name"
              placeholder="e.g. Cobalt Glass Vase"
              class="w-full p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>
          <div class="space-y-2">
            <label
              for="product_brand"
              class="block text-lg font-bold text-gray-400 uppercase tracking-widest"
              >Brand Identifier</label
            >
            <input
              type="text"
              id="product_brand"
              name="product_brand"
              placeholder="Brand source"
              class="w-full p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>

          <div class="space-y-2">
            <label
              for="category_name"
              class="block text-lg font-bold text-gray-400 uppercase tracking-widest"
              >Category</label
            >
            <select
              id="category_name"
              name="category_name"
              class="w-full p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none appearance-none"
              required
            >
              <option value="" disabled selected>Select category...</option>
              <option value="Electronics">Electronics</option>
              <option value="Hardware">Hardware</option>
              <option value="Plushie">Plushie</option>
            </select>
          </div>
          <div class="space-y-2">
            <label
              for="price"
              class="block text-lg font-bold text-gray-400 uppercase tracking-widest"
              >Unit Price (USD)</label
            >
            <div class="relative">
              <span class="absolute left-4 top-3.5 text-gray-400">$</span>
              <input
                type="number"
                step="0.01"
                id="price"
                name="price"
                placeholder="0.00"
                class="w-full p-3 pl-8 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none"
                required
              />
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-8">
          <div class="space-y-2">
            <label
              for="product_image"
              class="block text-lg font-bold text-gray-400 uppercase tracking-widest"
              >Technical Image</label
            >
            <input
              type="file"
              id="product_image"
              name="product_image"
              accept="image/*"
              class="w-full p-2 bg-[#E5E9ED] rounded text-xs file:bg-[#4A607C] file:text-white file:border-none file:px-4 file:py-1 file:rounded file:mr-4"
              required
            />
          </div>
        </div>

        <div class="bg-[#F1F5F9] p-8 rounded-xl border border-gray-100">
          <div class="flex items-center gap-6">
            <div class="bg-white p-3 rounded shadow-sm">
              <span class="text-xl">📋</span>
            </div>
            <div class="flex-1">
              <label
                for="quantity"
                class="block text-lg font-bold text-gray-400 uppercase tracking-widest mb-4"
                >Initial Stock Level</label
              >
              <div class="flex items-center gap-6">
                <input
                  type="range"
                  id="quantity"
                  name="quantity"
                  min="0"
                  max="1000"
                  bind:value={stockLevel}
                  class="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-[#4A607C]"
                />
                <div
                  class="bg-white px-4 py-2 border border-gray-200 rounded font-mono text-gray-700 w-20 text-center"
                >
                  {stockLevel}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </form>

    <div class="px-10 py-6 border-t border-gray-50 flex justify-center gap-12">
      <div
        class="flex items-center gap-2 text-lg font-bold text-gray-400 uppercase tracking-widest"
      >
        <span>🛡️</span> Secure Entry
      </div>
      <div
        class="flex items-center gap-2 text-lg font-bold text-gray-400 uppercase tracking-widest"
      >
        <span>🕒</span> Audit Logged
      </div>
      <div
        class="flex items-center gap-2 text-lg font-bold text-gray-400 uppercase tracking-widest"
      >
        <span>☁️</span> Real-time Sync
      </div>
    </div>
  </div>
</main>
