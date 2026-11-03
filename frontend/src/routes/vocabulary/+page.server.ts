import { backendGet } from '$lib/server/backend';
import type { SavedWord } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, depends }) => {
  depends('app:words');
  const [words, due] = await Promise.all([
    backendGet<SavedWord[]>(cookies, '/words'),
    backendGet<SavedWord[]>(cookies, '/words/review')
  ]);
  return { words, dueCount: due?.length ?? 0 };
};
