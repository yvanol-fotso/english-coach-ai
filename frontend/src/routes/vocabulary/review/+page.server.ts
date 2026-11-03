import { backendGet } from '$lib/server/backend';
import type { SavedWord } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => ({
  queue: await backendGet<SavedWord[]>(cookies, '/words/review')
});
