<script>
  import { enhance } from "$app/forms";
  import fuhuaWorking from "$lib/assets/working.png";
</script>

<main class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
  <div
    class="max-w-7xl w-full bg-white rounded-lg shadow-2xl overflow-hidden flex flex-col md:flex-row"
  >
    <section
      class="md:w-5/12 bg-[#4A607C] text-white p-10 flex flex-col justify-between"
    >
      <div>
        <h1 class="text-5xl font-bold leading-tight">
          Inventory<br />Inventory
        </h1>
        <p class="mt-4 text-gray-200 text-base leading-relaxed">
          Precision in every unit. Establish your organizational core with our
          architectural inventory framework.
        </p>

        <div class="mt-12 space-y-8">
          <div class="flex items-start gap-4">
            <span class="mt-1">📐</span>
            <div>
              <h3 class="font-semibold text-xl">Modular Foundation</h3>
              <p class="text-base text-gray-300">
                Scale from singular units to global logistics effortlessly.
              </p>
            </div>
          </div>
          <div class="flex items-start gap-4">
            <span class="mt-1">📊</span>
            <div>
              <h3 class="font-semibold text-xl">Deep Audit Trailing</h3>
              <p class="text-base text-gray-300">
                Maintain complete visibility over every asset movement.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-12">
        <img
          src={fuhuaWorking}
          alt="Warehouse"
          class="rounded shadow-lg w-full object-cover"
        />
      </div>
    </section>

    <section class="md:w-7/12 p-10">
      <h2 class="text-3xl font-bold text-gray-800">Finalize Your Account</h2>
      <p class="text-gray-500 text-base mt-1">
        Please provide the structural details for your Monolith instance.
      </p>

      <form method="POST" action="?/register" use:enhance class="mt-4 md:mt-16 space-y-5">
        <div>
          <label
            for="org"
            class="block text-base font-bold text-gray-500 uppercase tracking-wider"
            >Organization Name</label
          >
          <input
            type="text"
            id="org"
            name="organization_name"
            placeholder="e.g. Sin's Global Logistics"
            class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          />
        </div>

        <div>
          <label
            for="admin"
            class="block text-base font-bold text-gray-500 uppercase tracking-wider"
            >Administrator Name</label
          >
          <input
            type="text"
            id="admin"
            name="username"
            placeholder="Full legal name"
            class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          />
        </div>

        <div>
          <label
            for="email"
            class="block text-base font-bold text-gray-500 uppercase tracking-wider"
            >Email Address</label
          >
          <input
            type="email"
            id="email"
            name="email"
            placeholder="admin@organization.com"
            class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              for="pass"
              class="block text-base font-bold text-gray-500 uppercase tracking-wider"
              >Password</label
            >
            <input
              type="password"
              id="pass"
              name="password"
              placeholder="••••••••"
              class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>
          <div>
            <label
              for="confirm"
              class="block text-base font-bold text-gray-500 uppercase tracking-wider"
              >Confirm Password</label
            >
            <input
              type="password"
              id="confirm"
              name="confirm_password"
              placeholder="••••••••"
              class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>
        </div>

        <div>
          <label for="avatar" class="block text-base font-bold text-gray-500 uppercase tracking-wider">Avatar (Optional)</label>
          <input 
            type="file" 
            id="avatar" 
            name="user_avatar" 
            accept="image/*"
            class="w-full mt-1 p-2 text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-[#4A607C] file:text-white hover:file:bg-[#3d4f66] cursor-pointer bg-[#E5E9ED] rounded"
          />
        </div>

        <button
          type="submit"
          class="mt-4 md:mt-16 w-full bg-[#4A607C] hover:bg-[#3d4f66] text-white font-bold py-4 rounded shadow-md flex items-center justify-center gap-2 transition-colors"
        >
          Complete Setup <span>→</span>
        </button>
      </form>

      <p
        class="mt-4 md:mt-24 text-base text-gray-400 text-center md:text-left leading-relaxed"
      >
        By completing setup, you agree to our <a href="/" class="underline"
          >Terms of Service</a
        >
        and <a href="/" class="underline">Privacy Architecture</a>.
      </p>
    </section>
  </div>
</main>

