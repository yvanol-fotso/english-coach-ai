const LOCALES: Record<string, string> = {
  en: 'en-US',
  fr: 'fr-FR',
  es: 'es-ES',
  de: 'de-DE',
  pt: 'pt-PT',
  it: 'it-IT',
  zh: 'zh-CN',
  ar: 'ar-SA'
};

export const localeOf = (code: string): string => LOCALES[code] ?? 'en-US';

import type { CatalogLanguage } from '$lib/types';

/** Used when the backend catalog cannot be loaded, so the first-run screen still works. */
export const FALLBACK_LANGUAGES: CatalogLanguage[] = [
  { code: 'en', native: 'English', locale: 'en-US', label: { fr: 'Anglais', en: 'English' }, available: true },
  { code: 'fr', native: 'Français', locale: 'fr-FR', label: { fr: 'Français', en: 'French' }, available: true },
  { code: 'es', native: 'Español', locale: 'es-ES', label: { fr: 'Espagnol', en: 'Spanish' }, available: true }
];
