import type { Actions } from "@sveltejs/kit";
// import { BACKEND_URL } from "$env/static/private"

export const actions = {
    register: async({request})=>{
        const data = await request.formData();


    }
} satisfies Actions