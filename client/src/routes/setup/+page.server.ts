import type { Actions } from "@sveltejs/kit";

export const actions = {
    register: async({request})=>{
        const data = await request.formData();
        console.log(request)
        console.log(data);
    }
} satisfies Actions