import type { Cookies } from '@sveltejs/kit';
import type { Accent, Lang, Prefs, Theme } from '$lib/types';

const pick = <T extends string>(value: string | undefined, allowed: readonly T[], fallback: T): T =>
  allowed.includes(value as T) ? (value as T) : fallback;

export function readPrefs(cookies: Cookies, acceptLanguage: string | null): Prefs {
  const guess: Lang = acceptLanguage?.toLowerCase().startsWith('en') ? 'en' : 'fr';
  return {
    lang: pick(cookies.get('ec_lang'), ['fr', 'en'], guess),
    theme: pick<Theme>(cookies.get('ec_theme'), ['system', 'light', 'dark'], 'system'),
    accent: pick<Accent>(cookies.get('ec_accent'), ['teal', 'blue', 'plum', 'ember'], 'teal'),
    target: /^[a-z]{2}$/.test(cookies.get('ec_target') ?? '') ? (cookies.get('ec_target') as string) : 'en'
  };
}
