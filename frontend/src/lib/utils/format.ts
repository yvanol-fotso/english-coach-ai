import { t } from '$lib/i18n/index.svelte';
import type { Text } from '$lib/types';
import { preferences } from '$lib/stores/preferences.svelte';

export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat(preferences.lang, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(iso));
}

export function formatDay(iso: string): string {
  return new Intl.DateTimeFormat(preferences.lang, { day: 'numeric', month: 'short' }).format(new Date(iso));
}

export const pick = (text: Text): string => text[preferences.lang] ?? text.en;

export const langName = (code: string): string => {
  const key = `lang.${code}`;
  const text = t(key);
  return text === key ? code.toUpperCase() : text;
};
