export type WordStatus = 'ok' | 'missing' | 'extra';
export interface DiffWord {
  word: string;
  status: WordStatus;
}

const words = (text: string) =>
  text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}'\s]/gu, ' ')
    .split(/\s+/)
    .filter(Boolean);

export function compare(target: string, spoken: string): { words: DiffWord[]; score: number } {
  const a = words(target);
  const b = words(spoken);
  const table = Array.from({ length: a.length + 1 }, () => new Array<number>(b.length + 1).fill(0));
  for (let i = a.length - 1; i >= 0; i--)
    for (let j = b.length - 1; j >= 0; j--)
      table[i][j] = a[i] === b[j] ? table[i + 1][j + 1] + 1 : Math.max(table[i + 1][j], table[i][j + 1]);

  const result: DiffWord[] = [];
  let i = 0;
  let j = 0;
  while (i < a.length || j < b.length) {
    if (i < a.length && j < b.length && a[i] === b[j]) result.push({ word: a[i++], status: 'ok' }), j++;
    else if (j < b.length && (i === a.length || table[i][j + 1] >= table[i + 1][j])) result.push({ word: b[j++], status: 'extra' });
    else result.push({ word: a[i++], status: 'missing' });
  }
  const score = a.length ? Math.round((table[0][0] / a.length) * 100) : 0;
  return { words: result, score };
}

export const sameText = (a: string, b: string) => words(a).join(' ') === words(b).join(' ');
