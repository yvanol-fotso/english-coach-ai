import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, parent }) => {
  const { catalog } = await parent();
  if (catalog && !catalog.units.some((unit) => unit.id === params.unit)) error(404);
  return { unit: params.unit };
};
