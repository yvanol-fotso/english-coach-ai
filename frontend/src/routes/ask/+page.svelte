<script lang="ts">
  import AnswerCard from '$lib/components/ask/AnswerCard.svelte';
  import ChoiceGroup from '$lib/components/ui/ChoiceGroup.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { ask, codeOf } from '$lib/services/api';
  import { canDictate, dictate, speakSequence, type DictationStatus } from '$lib/services/speech';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { settings, type AnswerMode } from '$lib/stores/settings.svelte';
  import type { QuickAnswer } from '$lib/types';
  import { langName } from '$lib/utils/format';

  let question = $state('');
  let detail = $state<'short' | 'full'>('short');
  let micNative = $state(true);
  let status = $state<DictationStatus>('idle');
  let loading = $state(false);
  let errorCode = $state('');
  let history = $state<{ question: string; answer: QuickAnswer }[]>([]);
  let stopDictation: (() => void) | null = null;

  const micLocale = $derived(micNative ? preferences.nativeLocale : preferences.locale);

  const speakAnswer = (answer: QuickAnswer) =>
    speakSequence(
      [{ text: answer.spoken, lang: preferences.nativeLocale }, ...answer.examples.slice(0, 2).map((text) => ({ text, lang: preferences.locale }))],
      { rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName }
    );

  async function run(text = question) {
    const asked = text.trim();
    if (!asked || loading) return;
    loading = true;
    errorCode = '';
    try {
      const answer = await ask(asked, settings.level, detail);
      history = [{ question: asked, answer }, ...history].slice(0, 10);
      question = '';
      if (settings.answerMode !== 'text') void speakAnswer(answer);
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }

  function listen() {
    if (status === 'listening') return stopDictation?.();
    stopDictation = dictate({
      lang: micLocale,
      server: settings.serverStt,
      autoStop: true,
      onText: (heard) => (question = heard),
      onFinal: (heard) => {
        question = heard;
        void run(heard);
      },
      onStatus: (s) => (status = s)
    });
  }
</script>

<svelte:head><title>{t('nav.ask')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('ask.title')}</h1>
    <p class="lead">{t('ask.lead')}</p>
  </div>

  <form class="row" onsubmit={(event) => { event.preventDefault(); void run(); }}>
    {#if canDictate(settings.serverStt)}
      <button type="button" class="orb" class:live={status === 'listening'} aria-label={t('ask.mic')} aria-pressed={status === 'listening'} disabled={status === 'processing'} onclick={listen}>
        <Icon name="mic" size={22} />
      </button>
    {/if}
    <input class="field q" bind:value={question} placeholder={status === 'listening' ? t('ask.listening') : t('ask.placeholder')} maxlength="600" />
    <button class="btn btn-primary" disabled={loading || !question.trim()}>{loading ? t('ask.loading') : t('ask.submit')}</button>
  </form>

  {#if canDictate(settings.serverStt)}
    <button class="link-btn lang" onclick={() => (micNative = !micNative)}>
      {t('mic.lang', { lang: langName(micNative ? preferences.lang : preferences.target) })}
    </button>
  {/if}

  <div class="row options">
    <ChoiceGroup
      label={t('ask.mode')}
      value={settings.answerMode}
      options={[{ value: 'text', label: t('ask.mode.text') }, { value: 'voice', label: t('ask.mode.voice') }, { value: 'both', label: t('ask.mode.both') }]}
      onchange={(value) => (settings.answerMode = value)}
    />
    <ChoiceGroup
      label={t('ask.detail')}
      value={detail}
      options={[{ value: 'short', label: t('ask.short') }, { value: 'full', label: t('ask.full') }]}
      onchange={(value) => (detail = value as 'short' | 'full')}
    />
    <LevelSelect />
  </div>

  {#if errorCode}<ErrorNotice code={errorCode} onretry={() => run()} />{/if}

  {#each history as item (item.answer)}
    <AnswerCard question={item.question} answer={item.answer} mode={settings.answerMode} onplay={() => speakAnswer(item.answer)} />
  {/each}
</section>

<style>
  .q { flex: 1; min-width: 12rem; width: auto; }
  .options { align-items: flex-end; gap: 1.5rem; }
  .lang { justify-self: start; }
  .orb { width: 3rem; height: 3rem; flex: none; border-radius: 50%; border: 0; cursor: pointer; display: grid; place-items: center; background: var(--hl); color: var(--hl-ink); }
  .orb.live { background: var(--bad); color: #fff; animation: pulse 1.4s ease-out infinite; }
  @keyframes pulse { 0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--bad) 55%, transparent); } 100% { box-shadow: 0 0 0 16px transparent; } }
</style>
