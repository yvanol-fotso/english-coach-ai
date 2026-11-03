import type { Accent, Lang, Prefs, Theme } from '$lib/types';
import { setCookie } from '$lib/utils/cookies';

class Preferences {
  lang = $state<Lang>('fr');
  theme = $state<Theme>('system');
  accent = $state<Accent>('teal');

  init(prefs: Prefs) {
    this.lang = prefs.lang;
    this.theme = prefs.theme;
    this.accent = prefs.accent;
  }

  setLang(lang: Lang) {
    this.lang = lang;
    setCookie('ec_lang', lang);
    document.documentElement.lang = lang;
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
