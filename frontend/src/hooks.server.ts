import type { Handle, HandleServerError } from '@sveltejs/kit';
import { readPrefs } from '$lib/server/prefs';

const DESCRIPTIONS = {
  fr: "Un coach de langues privé qui tourne sur ton ordinateur : parle à voix haute, sois corrigé, écoute la réponse. Gratuit, sans abonnement.",
  en: 'A private language coach that runs on your computer: speak out loud, get corrected, hear the answer. Free, no subscription.'
} as const;

export const handle: Handle = async ({ event, resolve }) => {
  const prefs = readPrefs(event.cookies, event.request.headers.get('accept-language'));
  event.locals.prefs = prefs;

  const response = await resolve(event, {
    transformPageChunk: ({ html }) =>
      html
        .replaceAll('%lang%', prefs.lang)
        .replaceAll('%theme%', prefs.theme)
        .replaceAll('%accent%', prefs.accent)
        .replaceAll('%description%', DESCRIPTIONS[prefs.lang])
        .replaceAll('%origin%', event.url.origin)
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
