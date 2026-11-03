import { backendGet } from '$lib/server/backend';
import type { ConversationSummary } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, depends }) => {
  depends('app:history');
  return { conversations: await backendGet<ConversationSummary[]>(cookies, '/conversations') };
};
