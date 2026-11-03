<script lang="ts">
  import QuizCard from '$lib/components/practice/QuizCard.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, generateExercise, logActivity } from '$lib/services/api';
  import { canSpeak, speak, stopSpeaking } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { Exercise, PracticeKind } from '$lib/types';

  let kind = $state<PracticeKind>('reading');
  let topic = $state('');
  let current = $state<{ kind: PracticeKind; exercise: Exercise } | null>(null);
  let showText = $state(false);
  let loading = $state(false);
  let errorCode = $state('');

  async function run() {
    loading = true;
    errorCode = '';
    current = null;
    stopSpeaking();
    try {
      const exercise = await generateExercise(kind, settings.level, topic.trim());
      current = { kind, exercise };
      showText = kind === 'reading';
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }

  const record = (score: number, total: number) =>
    current && logActivity(current.kind, Math.round((score / total) * 100), { title: current.exercise.title, score, total }).catch(() => {});
</script>

<svelte:head><title>{t('nav.understand')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('practice.title')}</h1>
    <p class="lead">{t('practice.lead')}</p>
  </div>

  <div class="row">
    <div class="seg" role="group" aria-label={t('practice.title')}>
      <button aria-pressed={kind === 'reading'} onclick={() => (kind = 'reading')}>{t('practice.reading')}</button>
      <button aria-pressed={kind === 'listening'} onclick={() => (kind = 'listening')}>{t('practice.listening')}</button>
    </div>
    <LevelSelect />
  </div>
  <div class="row">
    <input class="field topic" bind:value={topic} placeholder={t('practice.topic')} maxlength="120" />
    <button class="btn btn-primary" onclick={run} disabled={loading}>{loading ? t('practice.loading') : t('practice.generate')}</button>
  </div>

  {#if errorCode}<ErrorNotice code={errorCode} onretry={run} />{/if}

  {#if current}
    <article class="card stack">
      <h2>{current.exercise.title}</h2>
      {#if current.kind === 'listening'}
        <div class="row">
          {#if canSpeak()}
            <button class="btn btn-primary" onclick={() => speak(current!.exercise.passage, { rate: settings.speechRate, server: settings.serverTts })}>{t('practice.play')}</button>
            <button class="btn" onclick={stopSpeaking}>{t('common.stop')}</button>
          {:else}
            <p class="muted">{t('practice.novoice')}</p>
          {/if}
          <button class="link-btn" onclick={() => (showText = !showText)}>{showText ? t('practice.hide') : t('practice.show')}</button>
        </div>
      {/if}
      {#if showText}<p class="passage">{current.exercise.passage}</p>{/if}
    </article>
    {#key current}<QuizCard questions={current.exercise.questions} onchecked={record} />{/key}
  {/if}
</section>

<style>
  .topic { flex: 1; min-width: 10rem; width: auto; }
  .passage { white-space: pre-wrap; }
</style>
