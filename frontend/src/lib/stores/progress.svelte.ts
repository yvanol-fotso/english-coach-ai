const KEY = 'english-coach:progress';
const MAX_ENTRIES = 2000;

export type Skill = 'speaking' | 'writing' | 'reading' | 'listening' | 'translation' | 'vocabulary';
interface Entry {
  skill: Skill;
  day: string;
}

const dayKey = (date: Date) => date.toLocaleDateString('en-CA');

class Progress {
  entries = $state<Entry[]>([]);
  #loaded = false;

  activeDays = $derived(new Set(this.entries.map((e) => e.day)));

  streak = $derived.by(() => {
    const cursor = new Date();
    if (!this.activeDays.has(dayKey(cursor))) cursor.setDate(cursor.getDate() - 1);
    let count = 0;
    while (this.activeDays.has(dayKey(cursor))) {
      count++;
      cursor.setDate(cursor.getDate() - 1);
    }
    return count;
  });

  countOf(skill: Skill) {
    return this.entries.filter((e) => e.skill === skill).length;
  }

  lastDays(length: number) {
    return Array.from({ length }, (_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - (length - 1 - i));
      const day = dayKey(date);
      return { day, count: this.entries.filter((e) => e.day === day).length };
    });
  }

  log(skill: Skill) {
    this.entries.push({ skill, day: dayKey(new Date()) });
    if (this.entries.length > MAX_ENTRIES) this.entries.splice(0, this.entries.length - MAX_ENTRIES);
  }

  load() {
    try {
      this.entries = JSON.parse(localStorage.getItem(KEY) ?? '[]');
    } catch {
      this.entries = [];
    }
    this.#loaded = true;
  }

  persist() {
    const snapshot = JSON.stringify(this.entries);
    if (this.#loaded) localStorage.setItem(KEY, snapshot);
  }
}

export const progress = new Progress();
