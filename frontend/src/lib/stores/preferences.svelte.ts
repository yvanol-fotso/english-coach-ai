import { localeOf } from '$lib/data/languages';
import type { Accent, Lang, Prefs, Theme } from '$lib/types';
import { setCookie } from '$lib/utils/cookies';

class Preferences {
  lang = $state<Lang>('fr');
  theme = $state<Theme>('system');
  accent = $state<Accent>('teal');
  target = $state('en');

  locale = $derived(localeOf(this.target));
  nativeLocale = $derived(localeOf(this.lang));

  init(prefs: Prefs) {
    this.lang = prefs.lang;
    this.theme = prefs.theme;
    this.accent = prefs.accent;
    this.target = prefs.target;
  }

  setLang(lang: Lang) {
    this.lang = lang;
    setCookie('ec_lang', lang);
    document.documentElement.lang = lang;
  }

  setTarget(code: string) {
    this.target = code;
    setCookie('ec_target', code);
  }

  setTheme(theme: Theme) {
    this.theme = theme;
    setCookie('ec_theme', theme);
    this.apply();
  }

  setAccent(accent: Accent) {
    this.accent = accent;
    setCookie('ec_accent', accent);
    this.apply();
  }

  apply() {
    const root = document.documentElement;
    const dark = this.theme === 'dark' || (this.theme === 'system' && matchMedia('(prefers-color-scheme: dark)').matches);
    root.dataset.theme = dark ? 'dark' : 'light';
    root.dataset.accent = this.accent;
  }
}

export const preferences = new Preferences();
