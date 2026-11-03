import { backendGet } from '$lib/server/backend';
import type { Stats } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
  const offset = Number(cookies.get('ec_tz') ?? 0) || 0;
  return { stats: await backendGet<Stats>(cookies, `/stats?tz_offset=${offset}`) };
};
