import { backendGet } from '$lib/server/backend';
import type { ActivityOut, Stats } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
  const offset = Number(cookies.get('ec_tz') ?? 0) || 0;
  const [stats, activities] = await Promise.all([
    backendGet<Stats>(cookies, `/stats?tz_offset=${offset}`),
    backendGet<ActivityOut[]>(cookies, '/activities?limit=30')
  ]);
  return { stats, activities: activities ?? [] };
};
