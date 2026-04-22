import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { APIResponse } from '$lib/types/api.types';
import { BACKEND_URL } from '$env/static/private';
import type { Products, UserBrief } from '$lib/types/types';

export const load: PageServerLoad = async ({ fetch }) => {
    const response = await fetch(`${BACKEND_URL}/user`, {
        method: 'GET',
        credentials: 'include'
    });

    const product = await fetch(`${BACKEND_URL}/products`, {
        method: 'GET',
        credentials: 'include'
    });

    if (!response.ok) {
        throw redirect(303, '/auth');
    }

    const result = await response.json() as APIResponse<UserBrief>;
    const product_result = await product.json() as APIResponse<Products>;

    const totalItems = product_result.data?.length ?? 0;
    const totalValue = product_result.data?.reduce((acc, item)=>{
        return acc + (Number(item.quantity) * Number(item.price))
    }, 0) ?? 0;

    return {
        user: result.data,
        product: product_result.data,
        img_url: BACKEND_URL,
        totalItems,
        totalValue
    };
};