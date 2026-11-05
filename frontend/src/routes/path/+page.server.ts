import { backendGet } from '$lib/server/backend';
import type { UnitProgress } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, locals, depends }) => {
  depends('app:course');
  return { progress: await backendGet<UnitProgress[]>(cookies, `/course?target=${locals.prefs.target}`) };
};
