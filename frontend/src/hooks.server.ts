import type { Handle, HandleServerError } from '@sveltejs/kit';
import { readPrefs } from '$lib/server/prefs';

export const handle: Handle = async ({ event, resolve }) => {
  const prefs = readPrefs(event.cookies, event.request.headers.get('accept-language'));
  event.locals.prefs = prefs;

  const response = await resolve(event, {
    transformPageChunk: ({ html }) =>
      html.replace('%lang%', prefs.lang).replace('%theme%', prefs.theme).replace('%accent%', prefs.accent)
  });
  response.headers.set('x-content-type-options', 'nosniff');
  response.headers.set('referrer-policy', 'same-origin');
  response.headers.set('permissions-policy', 'microphone=(self)');
  return response;
};

export const handleError: HandleServerError = ({ error, event }) => {
  console.error(`[${event.request.method}] ${event.url.pathname}`, error);
  return { message: 'internal' };
};
