import type { Feedback, Level } from '$lib/types';

export type AnswerMode = 'text' | 'voice' | 'both';

const KEY = 'english-coach:settings';

class Settings {
  level = $state<Level>('B1');
  speechRate = $state(0.9);
  feedback = $state<Feedback>('inline');
  autoSpeak = $state(true);
  answerMode = $state<AnswerMode>('both');
  voiceName = $state('');
  serverStt = $state(false);
  serverTts = $state(false);
  #loaded = false;

  load() {
    try {
      const saved = JSON.parse(localStorage.getItem(KEY) ?? '{}');
      if (saved.level) this.level = saved.level;
      if (saved.speechRate) this.speechRate = saved.speechRate;
      if (saved.feedback) this.feedback = saved.feedback;
      if (typeof saved.autoSpeak === 'boolean') this.autoSpeak = saved.autoSpeak;
      if (saved.answerMode) this.answerMode = saved.answerMode;
      if (typeof saved.voiceName === 'string') this.voiceName = saved.voiceName;
    } catch {
      /* corrupted storage is ignored */
    }
    this.#loaded = true;
  }

  persist() {
    const snapshot = JSON.stringify({
      level: this.level,
      speechRate: this.speechRate,
      feedback: this.feedback,
      autoSpeak: this.autoSpeak,
      answerMode: this.answerMode,
      voiceName: this.voiceName
    });
    if (this.#loaded) localStorage.setItem(KEY, snapshot);
  }
}

export const settings = new Settings();
