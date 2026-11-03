<script lang="ts">
  import { untrack } from 'svelte';
  import { invalidate } from '$app/navigation';
  import { page } from '$app/state';
  import ChatComposer from '$lib/components/chat/ChatComposer.svelte';
  import ChatThread from '$lib/components/chat/ChatThread.svelte';
  import ConversationRail from '$lib/components/chat/ConversationRail.svelte';
  import LivePanel from '$lib/components/chat/LivePanel.svelte';
  import TopicPicker from '$lib/components/chat/TopicPicker.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, getConversation, isAbort, streamChat } from '$lib/services/api';
  import { canDictate, dictate, speakSequence, speakable, stopSpeaking, type SpeechLang } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { ChatMessage } from '$lib/types';
  import { sameText } from '$lib/utils/diff';
  import { pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  let scenario = $state('free');
  let messages = $state<ChatMessage[]>([]);
  let conversationId = $state<number | null>(null);
  let busy = $state(false);
  let errorCode = $state('');
  let notice = $state('');
  let micLang = $state<SpeechLang>('en-US');
  let live = $state(false);
  let phase = $state<'listening' | 'thinking' | 'speaking'>('listening');
  let heard = $state('');
  let controller: AbortController | null = null;
  let stopListening: (() => void) | null = null;
  let emptyTurns = 0;
  let openedId: number | null = null;

  const situation = $derived(data.catalog?.scenarios.find((s) => s.id === scenario && s.chip));
  const toggleLang = () => (micLang = micLang === 'en-US' ? 'fr-FR' : 'en-US');

  function reset() {
    endLive();
    controller?.abort();
    messages = [];
    conversationId = null;
    scenario = 'free';
    errorCode = '';
    notice = '';
  }

  async function open(id: number) {
    reset();
    try {
      const conversation = await getConversation(id);
      scenario = conversation.scenario;
      conversationId = conversation.id;
      messages = conversation.messages.map(({ role, content, correction }) => ({ role, content, correction }));
    } catch (e) {
      errorCode = codeOf(e);
    }
  }

  $effect(() => {
    const raw = page.url.searchParams.get('c');
    const id = raw ? Number(raw) : null;
    if (id === openedId) return;
    openedId = id;
    untrack(() => (id ? open(id) : reset()));
  });

  async function send(text: string): Promise<boolean> {
    errorCode = '';
    messages.push({ role: 'user', content: text });
    const history = $state.snapshot(messages).map(({ role, content }) => ({ role, content }));
    const userMessage = messages[messages.length - 1];
    messages.push({ role: 'assistant', content: '' });
    const reply = messages[messages.length - 1];

    busy = true;
    controller = new AbortController();
    let ok = true;
    try {
      const request = { messages: history, conversation_id: conversationId, scenario, level: settings.level, feedback: settings.feedback };
      for await (const event of streamChat(request, controller.signal)) {
        if (event.type === 'conversation') conversationId = event.id;
        else if (event.type === 'correction') userMessage.correction = event.data;
        else reply.content += event.text;
      }
    } catch (e) {
      ok = false;
      if (!isAbort(e)) errorCode = codeOf(e);
    } finally {
      const produced = !!reply.content;
      if (!produced) messages.pop();
      busy = false;
      controller = null;
      invalidate('app:history');
      ok = ok && produced;
    }
    return ok;
  }

  async function speakReply(withCorrection: boolean) {
    const last = messages[messages.length - 1];
    const previous = messages[messages.length - 2];
    if (last?.role !== 'assistant') return;
    const parts: string[] = [];
    const fix = previous?.correction;
    if (withCorrection && fix && (fix.issues.length || !sameText(fix.corrected_text, previous.content))) {
      parts.push(`You can say: ${fix.corrected_text}`);
    }
    parts.push(speakable(last.content));
    await speakSequence(parts.filter(Boolean), { rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName });
  }

  async function submit(text: string) {
    const ok = await send(text);
    if (ok && settings.autoSpeak) await speakReply(false);
  }

  function startLive() {
    live = true;
    emptyTurns = 0;
    notice = '';
    listenTurn();
  }

  function endLive() {
    live = false;
    stopListening?.();
    stopListening = null;
    stopSpeaking();
    heard = '';
  }

  function listenTurn() {
    if (!live) return;
    phase = 'listening';
    heard = '';
    let got = false;
    stopListening = dictate({
      lang: micLang,
      server: settings.serverStt,
      autoStop: true,
      onText: (text) => (heard = text),
      onFinal: (text) => {
        got = true;
        emptyTurns = 0;
        void liveTurn(text);
      },
      onStatus: (status) => {
        if (status !== 'idle' || got || !live || phase !== 'listening') return;
        if (++emptyTurns >= 3) {
          endLive();
          notice = t('live.nospeech');
        } else setTimeout(listenTurn, 300);
      }
    });
  }

  async function liveTurn(text: string) {
    phase = 'thinking';
    const ok = await send(text);
    if (!live) return;
    if (!ok) return endLive();
    phase = 'speaking';
    await speakReply(true);
    if (live) listenTurn();
  }
</script>

<svelte:head><title>{t('nav.talk')} · English Coach</title></svelte:head>

<div class="layout">
  <ConversationRail items={data.conversations ?? []} activeId={conversationId} onnew={() => { reset(); history.replaceState(history.state, '', '/chat'); }} />

  <section class="chat">
    <header class="row bar">
      <LevelSelect />
      <label class="toggle">
        <input type="checkbox" checked={settings.feedback === 'inline'} onchange={(e) => (settings.feedback = e.currentTarget.checked ? 'inline' : 'off')} />
        {t('talk.feedback')}
      </label>
      <label class="toggle">
        <input type="checkbox" bind:checked={settings.autoSpeak} />
        {t('talk.autospeak')}
      </label>
      {#if situation}
        <button class="chip" aria-pressed="true" onclick={() => (scenario = 'free')}>{pick(situation.label)} ×</button>
      {/if}
      <span class="spacer"></span>
      {#if canDictate(settings.serverStt)}
        <button class="btn btn-primary" onclick={live ? endLive : startLive}>
          <Icon name="mic" size={18} /> {live ? t('live.end') : t('live.start')}
        </button>
      {/if}
    </header>

    {#if messages.length === 0}
      <TopicPicker catalog={data.catalog} {scenario} onstart={submit} onscenario={(id) => (scenario = id)} />
    {:else}
      <ChatThread {messages} {busy} />
    {/if}

    {#if notice}<p class="notice notice-warn">{notice}</p>{/if}
    {#if errorCode}<ErrorNotice code={errorCode} />{/if}

    {#if live}
      <LivePanel {phase} {heard} lang={micLang} onlang={toggleLang} onskip={stopSpeaking} onend={endLive} />
    {:else}
      <ChatComposer {busy} lang={micLang} onlang={toggleLang} onsend={submit} onstop={() => controller?.abort()} />
    {/if}
  </section>
</div>

<style>
  .layout { display: flex; height: 100%; }
  .chat { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 1rem; max-width: 52rem; margin-inline: auto; padding: clamp(1rem, 3vw, 2rem); }
  .bar { gap: 0.8rem; }
  .toggle { display: flex; align-items: center; gap: 0.5rem; font-size: 0.88rem; color: var(--muted); cursor: pointer; }
  .spacer { flex: 1; }
</style>
