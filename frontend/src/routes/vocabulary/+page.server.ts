import { backendGet } from '$lib/server/backend';
import type { SavedWord } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, depends, locals }) => {
  depends('app:words');
  const [words, due] = await Promise.all([
    backendGet<SavedWord[]>(cookies, `/words?language=${locals.prefs.target}`),
    backendGet<SavedWord[]>(cookies, `/words/review?language=${locals.prefs.target}`)
  ]);
  return { words, dueCount: due?.length ?? 0 };
};
