<script lang="ts">
  import { enhance } from "$app/forms";
</script>

<main class="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center p-4">
  <div class="bg-white rounded-sm shadow-xl border-t-4 border-[#4A607C] overflow-hidden">
    <div class="p-10 pt-12">
      <h1 class="text-4xl font-bold text-gray-800">Welcome back</h1>
      <p class="text-gray-500 text-lg mt-2">Enter your credentials to access the central repository.</p>

      <form method="POST" action="?/login" use:enhance class="mt-10 space-y-6">
        <div>
          <label for="username" class="block text-base font-bold text-gray-400 uppercase tracking-widest">Username / Email</label>
          <input 
            type="text" 
            id="username" 
            name="username" 
            placeholder="name@company.com" 
            class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-400" 
          />
        </div>

        <div>
          <div class="flex justify-between items-center">
            <label for="password" class="block text-base font-bold text-gray-400 uppercase tracking-widest">Password</label>
            <a href="/forgot-password" class="text-base font-bold text-[#4A607C] uppercase tracking-widest hover:underline">Forgot Password?</a>
          </div>
          <input 
            type="password" 
            id="password" 
            name="password" 
            placeholder="••••••••" 
            class="w-full mt-1 p-3 bg-[#E5E9ED] border-none rounded focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
          />
        </div>
        
        <!-- <label class="flex items-center gap-3 cursor-pointer group">
          <input type="checkbox" name="remember" class="w-4 h-4 border-gray-300 rounded text-[#4A607C] focus:ring-[#4A607C]" />
          <span class="text-base text-gray-500 group-hover:text-gray-700 transition-colors">Keep me authenticated for 30 days</span>
        </label> -->

        <button 
          type="submit" 
          class="w-full bg-[#4A607C] hover:bg-[#3d4f66] text-white font-bold py-4 rounded shadow-md flex items-center justify-center gap-2 transition-colors mt-8"
        >
          Sign In <span>→</span>
        </button>
      </form>

      <div class="mt-12 pt-6 border-t border-gray-100 text-center">
        <p class="text-base text-gray-500">
          New here? <a href="/register" class="text-[#4A607C] font-semibold hover:underline">Set up an account</a>
        </p>
      </div>
    </div>
  </div>

  <div class="mt-8 flex items-center gap-8 text-base font-bold text-gray-400 uppercase tracking-widest">
    <div class="flex items-center gap-2">
        <span class="w-8 bg-gray-200"></span>
        V 4.0.2
    </div>
    <div class="flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        Encrypted Session
    </div>
  </div>
</main>