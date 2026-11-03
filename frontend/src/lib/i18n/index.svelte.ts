import { preferences } from '$lib/stores/preferences.svelte';
import { en } from './en';
import { fr } from './fr';

const dictionaries: Record<string, Record<string, string>> = { fr, en };

export function t(key: string, vars?: Record<string, string | number>): string {
  let text = dictionaries[preferences.lang]?.[key] ?? fr[key as keyof typeof fr] ?? key;
  if (vars) for (const [name, value] of Object.entries(vars)) text = text.replaceAll(`{${name}}`, String(value));
  return text;
}

export const plural = (base: string, n: number) => t(n > 1 ? `${base}.many` : `${base}.one`, { n });
