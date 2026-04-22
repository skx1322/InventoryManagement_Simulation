import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { APIResponse } from '$lib/types/api.types';
import { BACKEND_URL } from '$env/static/private';
import type { Products, UserBrief } from '$lib/types/types';

export const load: PageServerLoad = async ({ fetch }) => {
  
};