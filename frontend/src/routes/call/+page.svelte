<script lang="ts">
  import { onDestroy } from 'svelte';
  import { invalidate } from '$app/navigation';
  import CallStage from '$lib/components/call/CallStage.svelte';
  import CallSummaryCard from '$lib/components/call/CallSummaryCard.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, getCallSummary } from '$lib/services/api';
  import { ConversationSession } from '$lib/services/conversation.svelte';
  import { canDictate } from '$lib/services/speech';
  import { VoiceLoop } from '$lib/services/voiceLoop.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { settings } from '$lib/stores/settings.svelte';
  import type { CallSummary } from '$lib/types';
  import { langName, pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  type Stage = 'setup' | 'ringing' | 'live' | 'summary';
  let stage = $state<Stage>('setup');
  let seconds = $state(0);
  let captionsOn = $state(true);
  let micNative = $state(false);
  let summary = $state<CallSummary | null>(null);
  let summaryState = $state<'idle' | 'loading' | 'empty' | 'error'>('idle');
  let summaryError = $state('');
  let timer: ReturnType<typeof setInterval> | null = null;

  const session = new ConversationSession(() => invalidate('app:history'));
  const loop = new VoiceLoop({
    lang: () => (micNative ? preferences.nativeLocale : preferences.locale),
    server: () => settings.serverStt,
    turn: (text) => session.send(text),
    speak: () => session.speakLast(true),
    onStall: () => {}
  });

  const scenarios = $derived(data.catalog?.scenarios ?? []);
  const scenario = $derived(scenarios.find((s) => s.id === session.scenario));
  const clock = $derived(`${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`);
  const micLabel = $derived(t('mic.lang', { lang: langName(micNative ? preferences.lang : preferences.target) }));
  const ready = $derived(canDictate(settings.serverStt));

  const stopTimer = () => {
    if (timer) clearInterval(timer);
    timer = null;
  };

  async function dial() {
    session.reset();
    summary = null;
    summaryState = 'idle';
    seconds = 0;
    stage = 'ringing';
    await new Promise((resolve) => setTimeout(resolve, 1400));
    stage = 'live';
    timer = setInterval(() => seconds++, 1000);
    await loop.start(() => session.send('', true));
  }

  async function hangUp() {
    loop.end();
    session.abort();
    stopTimer();
    stage = 'summary';
    const spoke = session.messages.some((m) => m.role === 'user');
    if (!session.id || !spoke) {
      summaryState = 'empty';
      return;
    }
    summaryState = 'loading';
    try {
      summary = await getCallSummary(session.id);
      summaryState = 'idle';
    } catch (e) {
      summaryError = codeOf(e);
      summaryState = 'error';
    }
  }

  onDestroy(() => {
    loop.end();
    session.abort();
    stopTimer();
  });
</script>

<svelte:head><title>{t('nav.call')} · English Coach</title></svelte:head>

<section class="page call-page">
  {#if stage === 'setup'}
    <div class="page-head">
      <h1>{t('call.title')}</h1>
      <p class="lead">{t('call.lead')}</p>
    </div>

    {#if !ready}<p class="notice notice-warn">{t('call.nomic')}</p>{/if}

    <div class="stack">
      <h2>{t('call.who')}</h2>
      <div class="row">
        {#each scenarios as s}
          <button class="chip" aria-pressed={session.scenario === s.id} onclick={() => (session.scenario = s.id)}>{pick(s.label)}</button>
        {/each}
      </div>
    </div>

    <div class="row">
      <LevelSelect />
      <label class="toggle">
        <input type="checkbox" checked={settings.feedback === 'inline'} onchange={(e) => (settings.feedback = e.currentTarget.checked ? 'inline' : 'off')} />
        {t('call.corrections')}
      </label>
    </div>

    <button class="btn btn-primary dial" onclick={dial} disabled={!ready || !data.catalog}><Icon name="phone" size={20} /> {t('call.dial')}</button>
  {:else if stage === 'ringing'}
    <div class="ringing"><p class="status">{t('call.ringing')}…</p></div>
  {:else if stage === 'live'}
    <CallStage
      title={scenario ? pick(scenario.label) : t('call.title')}
      time={clock}
      phase={loop.phase}
      active={loop.active}
      heard={loop.heard}
      captions={session.messages}
      showCaptions={captionsOn}
      muted={loop.muted}
      {micLabel}
      onmute={() => loop.setMuted(!loop.muted)}
      oncaptions={() => (captionsOn = !captionsOn)}
      onlang={() => (micNative = !micNative)}
      onskip={() => loop.skip()}
      onresume={() => loop.start()}
      onhangup={hangUp}
    />
    {#if session.errorCode}<ErrorNotice code={session.errorCode} />{/if}
  {:else}
    <h1>{t('call.summary')}</h1>
    {#if summaryState === 'loading'}
      <p class="muted">{t('call.loading')}…</p>
    {:else if summaryState === 'empty'}
      <p class="muted">{t('call.nothing')}</p>
    {:else if summaryState === 'error'}
      <ErrorNotice code={summaryError} />
    {:else if summary}
      <CallSummaryCard {summary} time={clock} />
    {/if}
    <div class="row">
      <button class="btn btn-primary" onclick={() => (stage = 'setup')}>{t('call.again')}</button>
      {#if session.id}<a class="btn" href="/chat?c={session.id}" style="text-decoration: none">{t('call.open')}</a>{/if}
    </div>
  {/if}
</section>

<style>
  .call-page { min-height: 100%; }
  .toggle { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--muted); cursor: pointer; }
  .dial { justify-self: start; display: inline-flex; align-items: center; gap: 0.6rem; padding: 0.8rem 1.6rem; font-size: 1.05rem; }
  .ringing { display: grid; place-items: center; min-height: 50vh; }
  .status { font: 650 1.4rem var(--font-display); animation: blink 1.2s ease-in-out infinite; }
  @keyframes blink { 50% { opacity: 0.4; } }
</style>
