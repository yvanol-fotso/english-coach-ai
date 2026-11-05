import { sameText } from '$lib/utils/diff';
import { preferences } from '$lib/stores/preferences.svelte';
import { settings } from '$lib/stores/settings.svelte';
import type { ChatMessage, ConversationDetail } from '$lib/types';
import { codeOf, isAbort, streamChat } from './api';
import { speakSequence, speakable } from './speech';

export class ConversationSession {
  messages = $state<ChatMessage[]>([]);
  id = $state<number | null>(null);
  scenario = $state('free');
  busy = $state(false);
  errorCode = $state('');

  #controller: AbortController | null = null;
  #onDone: () => void;

  constructor(onDone: () => void = () => {}) {
    this.#onDone = onDone;
  }

  reset() {
    this.abort();
    this.messages = [];
    this.id = null;
    this.scenario = 'free';
    this.errorCode = '';
  }

  load(detail: ConversationDetail) {
    this.reset();
    this.scenario = detail.scenario;
    this.id = detail.id;
    this.messages = detail.messages.map(({ role, content, correction }) => ({ role, content, correction }));
  }

  abort() {
    this.#controller?.abort();
  }

  /** Sends the learner's text (or opens a call when `opening` is true). Resolves true when a reply arrived. */
  async send(text: string, opening = false): Promise<boolean> {
    this.errorCode = '';
    if (!opening) this.messages.push({ role: 'user', content: text });
    const history = opening
      ? [{ role: 'user' as const, content: '(call started)' }]
      : $state.snapshot(this.messages).map(({ role, content }) => ({ role, content }));
    const userMessage = opening ? null : this.messages[this.messages.length - 1];
    this.messages.push({ role: 'assistant', content: '' });
    const reply = this.messages[this.messages.length - 1];

    this.busy = true;
    this.#controller = new AbortController();
    let ok = true;
    try {
      const request = {
        messages: history,
        conversation_id: this.id,
        scenario: this.scenario,
        level: settings.level,
        feedback: settings.feedback,
        opening
      };
      for await (const event of streamChat(request, this.#controller.signal)) {
        if (event.type === 'conversation') this.id = event.id;
        else if (event.type === 'correction' && userMessage) userMessage.correction = event.data;
        else if (event.type === 'token') reply.content += event.text;
      }
    } catch (e) {
      ok = false;
      if (!isAbort(e)) this.errorCode = codeOf(e);
    } finally {
      const produced = !!reply.content;
      if (!produced) this.messages.pop();
      this.busy = false;
      this.#controller = null;
      this.#onDone();
      ok = ok && produced;
    }
    return ok;
  }

  /** Speaks the last coach reply, optionally preceded by the corrected version of the learner's sentence. */
  async speakLast(withCorrection: boolean) {
    const last = this.messages[this.messages.length - 1];
    const previous = this.messages[this.messages.length - 2];
    if (last?.role !== 'assistant') return;
    const parts: string[] = [];
    const fix = previous?.correction;
    if (withCorrection && fix && (fix.issues.length || !sameText(fix.corrected_text, previous.content))) {
      parts.push(fix.corrected_text);
    }
    parts.push(speakable(last.content));
    await speakSequence(parts.filter(Boolean), {
      lang: preferences.locale,
      rate: settings.speechRate,
      server: settings.serverTts,
      voice: settings.voiceName
    });
  }
}
