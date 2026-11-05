import { backendGet } from '$lib/server/backend';
import type { SavedWord } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, locals }) => ({
  queue: await backendGet<SavedWord[]>(cookies, `/words/review?language=${locals.prefs.target}`)
});
