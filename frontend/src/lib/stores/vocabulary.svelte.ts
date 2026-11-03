import type { Explanation } from '$lib/types';

const KEY = 'english-coach:vocabulary';

class Vocabulary {
  words = $state<Explanation[]>([]);
  #loaded = false;

  has(term: string) {
    return this.words.some((w) => w.term.toLowerCase() === term.toLowerCase());
  }

  add(word: Explanation) {
    if (!this.has(word.term)) this.words.unshift($state.snapshot(word));
  }

  remove(term: string) {
    this.words = this.words.filter((w) => w.term !== term);
  }

  load() {
    try {
      this.words = JSON.parse(localStorage.getItem(KEY) ?? '[]');
    } catch {
      this.words = [];
    }
    this.#loaded = true;
  }

  persist() {
    const snapshot = JSON.stringify(this.words);
    if (this.#loaded) localStorage.setItem(KEY, snapshot);
  }
}

export const vocabulary = new Vocabulary();
