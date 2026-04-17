import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "@sveltejs/kit";
import { BACKEND_URL } from "$env/static/private"
import type { APIResponse } from "$lib/types/api.types";

export const actions = {
    login: async ({ request, fetch, cookies }) => {
        const data = await request.formData();
        const res = await fetch(`${BACKEND_URL}/auth/login`, {
            method: 'POST',
            body: data,
            credentials: 'include'
        });

        const result = await res.json() as APIResponse<{ username: string, token: string }>;
        console.log(result.success)
        if (!result.success || !result.data) {
            return fail(401, {
                message: result.message,
                error: true
            });
        }
        cookies.set('access_token', result.data.token, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            secure: false, // Set to true in production with HTTPS
            maxAge: 60 * 60 * 24 // 1 day
        });
        

        throw redirect(303, "/dashboard");
    }
} satisfies Actions