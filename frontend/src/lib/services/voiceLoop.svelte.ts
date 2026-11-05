import { dictate, stopSpeaking } from './speech';

export type VoicePhase = 'listening' | 'thinking' | 'speaking' | 'muted';

interface Config {
  lang: () => string;
  server: () => boolean;
  turn: (text: string) => Promise<boolean>;
  speak: () => Promise<void>;
  onStall: () => void;
}

export class VoiceLoop {
  active = $state(false);
  phase = $state<VoicePhase>('listening');
  heard = $state('');
  muted = $state(false);

  #config: Config;
  #stop: (() => void) | null = null;
  #empty = 0;

  constructor(config: Config) {
    this.#config = config;
  }

  async start(opening?: () => Promise<boolean>) {
    this.active = true;
    this.muted = false;
    this.#empty = 0;
    if (opening) {
      this.phase = 'thinking';
      const ok = await opening();
      if (!this.active) return;
      if (!ok) return this.end();
      this.phase = 'speaking';
      await this.#config.speak();
    }
    this.#listen();
  }

  end() {
    this.active = false;
    this.#stop?.();
    this.#stop = null;
    stopSpeaking();
    this.heard = '';
  }

  skip() {
    stopSpeaking();
  }

  setMuted(value: boolean) {
    this.muted = value;
    if (value) {
      this.#stop?.();
      this.#stop = null;
      this.phase = 'muted';
    } else if (this.active && this.phase === 'muted') {
      this.#listen();
    }
  }

  #listen() {
    if (!this.active) return;
    if (this.muted) {
      this.phase = 'muted';
      return;
    }
    this.phase = 'listening';
    this.heard = '';
    let cancelled = false;
    let got = false;

    const stop = dictate({
      lang: this.#config.lang(),
      server: this.#config.server(),
      autoStop: true,
      onText: (text) => (this.heard = text),
      onFinal: (text) => {
        if (cancelled || !this.active) return;
        got = true;
        this.#empty = 0;
        void this.#turn(text);
      },
      onStatus: (status) => {
        if (status !== 'idle' || got || cancelled || !this.active || this.phase !== 'listening') return;
        if (++this.#empty >= 3) {
          this.end();
          this.#config.onStall();
        } else setTimeout(() => this.#listen(), 300);
      }
    });
    this.#stop = () => {
      cancelled = true;
      stop();
    };
  }

  async #turn(text: string) {
    this.phase = 'thinking';
    const ok = await this.#config.turn(text);
    if (!this.active) return;
    if (!ok) return this.end();
    this.phase = 'speaking';
    await this.#config.speak();
    this.#listen();
  }
}
