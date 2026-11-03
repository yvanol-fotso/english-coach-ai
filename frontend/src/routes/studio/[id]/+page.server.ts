import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, parent }) => {
  const { catalog } = await parent();
  if (catalog && !catalog.tools.some((tool) => tool.id === params.id)) error(404);
  return { id: params.id };
};
