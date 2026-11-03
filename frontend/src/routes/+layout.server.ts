import { backendGet, getHealth, PROFILE_COOKIE } from '$lib/server/backend';
import type { Catalog } from '$lib/types';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ fetch, cookies, locals, depends }) => {
  depends('app:health');
  return {
    health: await getHealth(fetch),
    catalog: await backendGet<Catalog>(cookies, '/catalog'),
    prefs: locals.prefs,
    profile: cookies.get(PROFILE_COOKIE) ?? null
  };
};
