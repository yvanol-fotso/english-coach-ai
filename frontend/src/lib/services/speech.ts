import { localeOf } from '$lib/data/languages';
import { preferences } from '$lib/stores/preferences.svelte';

export type SpeechLang = string;
export type DictationStatus = 'idle' | 'listening' | 'processing';

interface SpeakOptions {
  rate?: number;
  lang?: SpeechLang;
  server?: boolean;
  voice?: string;
}

interface DictateOptions {
  lang: SpeechLang;
  server: boolean;
  autoStop?: boolean;
  onText?: (text: string) => void;
  onFinal?: (text: string) => void;
  onStatus: (status: DictationStatus) => void;
}

interface RecognitionLike {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult: ((event: any) => void) | null;
  onend: (() => void) | null;
  onerror: (() => void) | null;
  start(): void;
  stop(): void;
}

let session = 0;
let cancelCurrent: (() => void) | null = null;

const hasSynthesis = () => 'speechSynthesis' in globalThis;

function recognitionCtor(): (new () => RecognitionLike) | undefined {
  const w = globalThis as any;
  return w.SpeechRecognition ?? w.webkitSpeechRecognition;
}

export const canSpeak = () => hasSynthesis() || typeof Audio !== 'undefined';

export const canDictate = (server: boolean) =>
  server ? !!globalThis.navigator?.mediaDevices && 'MediaRecorder' in globalThis : !!recognitionCtor();

export function listVoices(language = 'en'): SpeechSynthesisVoice[] {
  return hasSynthesis() ? speechSynthesis.getVoices().filter((v) => v.lang.toLowerCase().startsWith(language)) : [];
}

function pickVoice(lang: SpeechLang, preferred: string): SpeechSynthesisVoice | undefined {
  const voices = listVoices(lang.slice(0, 2));
  return (
    voices.find((v) => v.name === preferred) ??
    voices.find((v) => /natural|online/i.test(v.name)) ??
    voices.find((v) => /google/i.test(v.name)) ??
    voices.find((v) => v.lang === lang) ??
    voices[0]
  );
}

export function stopSpeaking(): void {
  session++;
  cancelCurrent?.();
}

function play(text: string, { rate = 0.9, lang = preferences.locale, server = false, voice = '' }: SpeakOptions): Promise<void> {
  return new Promise<void>((resolve) => {
    let finished = false;
    let audio: HTMLAudioElement | null = null;
    const done = () => {
      if (finished) return;
      finished = true;
      cancelCurrent = null;
      resolve();
    };
    cancelCurrent = () => {
      audio?.pause();
      if (hasSynthesis()) speechSynthesis.cancel();
      done();
    };

    const inBrowser = () => {
      if (finished) return;
      if (!hasSynthesis()) return done();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      utterance.rate = rate;
      const chosen = pickVoice(lang, voice);
      if (chosen) utterance.voice = chosen;
      utterance.onend = done;
      utterance.onerror = done;
      speechSynthesis.speak(utterance);
    };

    if (!(server && lang === 'en-US')) return inBrowser();

    fetch('/api/speech/synthesize', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text })
    })
      .then(async (res) => {
        if (finished) return;
        if (!res.ok) return inBrowser();
        const url = URL.createObjectURL(await res.blob());
        audio = new Audio(url);
        audio.playbackRate = rate;
        audio.onended = () => {
          URL.revokeObjectURL(url);
          done();
        };
        audio.onerror = inBrowser;
        await audio.play();
      })
      .catch(inBrowser);
  });
}

export function speak(text: string, options: SpeakOptions = {}): Promise<void> {
  stopSpeaking();
  return play(text, options);
}

export async function speakSequence(parts: (string | { text: string; lang?: SpeechLang })[], options: SpeakOptions = {}): Promise<void> {
  stopSpeaking();
  const id = session;
  for (const part of parts) {
    if (id !== session) return;
    await play(typeof part === 'string' ? part : part.text, typeof part === 'string' ? options : { ...options, lang: part.lang ?? options.lang });
  }
}

export { localeOf };

export const speakable = (text: string) => text.replace(/\([^)]*\)/g, ' ').replace(/[*_#]/g, '').replace(/\s+/g, ' ').trim();

function dictateInBrowser({ lang, onText, onFinal, onStatus }: DictateOptions): () => void {
  const Ctor = recognitionCtor();
  if (!Ctor) {
    onStatus('idle');
    return () => {};
  }
  const recognition = new Ctor();
  recognition.lang = lang;
  recognition.interimResults = true;
  recognition.continuous = false;
  let last = '';
  recognition.onresult = (event) => {
    last = Array.from(event.results as ArrayLike<any>, (r) => r[0].transcript).join(' ').trim();
    onText?.(last);
  };
  recognition.onend = () => {
    if (last) onFinal?.(last);
    onStatus('idle');
  };
  recognition.start();
  onStatus('listening');
  return () => recognition.stop();
}

function watchSilence(stream: MediaStream, onDone: (spoke: boolean) => void): () => void {
  const context = new AudioContext();
  const analyser = context.createAnalyser();
  analyser.fftSize = 1024;
  context.createMediaStreamSource(stream).connect(analyser);
  const data = new Uint8Array(analyser.fftSize);
  const started = performance.now();
  let spoke = false;
  let lastVoice = 0;

  const timer = setInterval(() => {
    analyser.getByteTimeDomainData(data);
    let sum = 0;
    for (const value of data) sum += ((value - 128) / 128) ** 2;
    const now = performance.now();
    if (Math.sqrt(sum / data.length) > 0.02) {
      spoke = true;
      lastVoice = now;
    }
    const silent = spoke && now - lastVoice > 1400;
    const waited = !spoke && now - started > 8000;
    if (silent || waited || now - started > 30000) {
      clearInterval(timer);
      context.close();
      onDone(spoke);
    }
  }, 100);
  return () => {
    clearInterval(timer);
    context.close().catch(() => {});
  };
}

function dictateWithServer({ lang, autoStop, onText, onFinal, onStatus }: DictateOptions): () => void {
  let recorder: MediaRecorder | null = null;
  let cancelled = false;
  onStatus('listening');

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      if (cancelled) {
        stream.getTracks().forEach((t) => t.stop());
        return onStatus('idle');
      }
      const chunks: Blob[] = [];
      const rec = new MediaRecorder(stream);
      recorder = rec;
      let spoke = true;
      let stopWatching: (() => void) | null = null;

      rec.ondataavailable = (e) => chunks.push(e.data);
      rec.onstop = async () => {
        stopWatching?.();
        stream.getTracks().forEach((t) => t.stop());
        if (!spoke) return onStatus('idle');
        onStatus('processing');
        try {
          const form = new FormData();
          form.append('file', new Blob(chunks, { type: rec.mimeType }), 'speech.webm');
          form.append('language', lang.slice(0, 2));
          const res = await fetch('/api/speech/transcribe', { method: 'POST', body: form });
          const text = res.ok ? String((await res.json()).text ?? '').trim() : '';
          if (text) {
            onText?.(text);
            onFinal?.(text);
          }
        } finally {
          onStatus('idle');
        }
      };
      rec.start();
      if (autoStop) {
        stopWatching = watchSilence(stream, (heard) => {
          spoke = heard;
          if (rec.state !== 'inactive') rec.stop();
        });
      }
    })
    .catch(() => onStatus('idle'));

  return () => {
    cancelled = true;
    if (recorder && recorder.state !== 'inactive') recorder.stop();
  };
}

export const dictate = (options: DictateOptions) =>
  options.server && canDictate(true) ? dictateWithServer(options) : dictateInBrowser(options);
