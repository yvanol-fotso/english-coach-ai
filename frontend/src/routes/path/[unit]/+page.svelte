<script lang="ts">
  import { onMount } from 'svelte';
  import { invalidate } from '$app/navigation';
  import DialogueView from '$lib/components/path/DialogueView.svelte';
  import PhraseList from '$lib/components/path/PhraseList.svelte';
  import PronunciationCard from '$lib/components/practice/PronunciationCard.svelte';
  import QuizCard from '$lib/components/practice/QuizCard.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, completeLesson, getLesson } from '$lib/services/api';
  import { canDictate } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { Lesson } from '$lib/types';
  import { pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  const steps = ['discover', 'repeat', 'dialogue', 'quiz', 'done'] as const;
  let lesson = $state<Lesson | null>(null);
  let errorCode = $state('');
  let loading = $state(true);
  let step = $state(0);
  let phraseIndex = $state(0);
  let repeatScores = $state<number[]>([]);
  let repeatScored = $state(false);
  let quizScore = $state<number | null>(null);
  let saved = $state(false);

  const unit = $derived(data.catalog?.units.find((u) => u.id === data.unit));
  const nextUnit = $derived.by(() => {
    const units = data.catalog?.units ?? [];
    return units[units.findIndex((u) => u.id === data.unit) + 1];
  });
  const canRepeat = $derived(canDictate(settings.serverStt));
  const parts = $derived([quizScore, repeatScores.length ? repeatScores.reduce((a, b) => a + b, 0) / repeatScores.length : null].filter((v): v is number => v !== null));
  const finalScore = $derived(parts.length ? Math.round(parts.reduce((a, b) => a + b, 0) / parts.length) : 0);

  async function load() {
    loading = true;
    errorCode = '';
    try {
      lesson = await getLesson(data.unit);
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }

  function next() {
    if (step === 0 && !canRepeat) step = 2;
    else step++;
  }

  function nextPhrase() {
    if (!lesson) return;
    if (phraseIndex + 1 < lesson.phrases.length) {
      phraseIndex++;
      repeatScored = false;
    } else next();
  }

  async function finish() {
    try {
      await completeLesson(data.unit, finalScore);
      saved = true;
      await invalidate('app:course');
    } catch (e) {
      errorCode = codeOf(e);
    }
  }

  onMount(load);
</script>

<svelte:head><title>{unit ? pick(unit.title) : t('nav.path')} · English Coach</title></svelte:head>

<section class="page">
  <a class="link-btn back" href="/path">← {t('path.back')}</a>

  {#if unit}
    <div class="page-head">
      <h1>{pick(unit.title)}</h1>
      <p class="lead">{t('path.goal')} : {pick(unit.goal)}</p>
    </div>
  {/if}

  <ol class="steps" aria-label="Steps">
    {#each steps as name, i}<li class:on={i === step} class:past={i < step}>{t(`path.step.${name}`)}</li>{/each}
  </ol>

  {#if loading}
    <p class="muted">{t('path.loading')}</p>
  {:else if errorCode && !lesson}
    <ErrorNotice code={errorCode} onretry={load} />
  {:else if lesson}
    {#if step === 0}
      <p>{lesson.intro}</p>
      <PhraseList phrases={lesson.phrases} />
      <button class="btn btn-primary" style="justify-self: start" onclick={next}>{t('path.next')}</button>
    {:else if step === 1}
      <p class="muted">{t('drills.progress', { i: phraseIndex + 1, n: lesson.phrases.length })}</p>
      {#key phraseIndex}
        <PronunciationCard sentence={lesson.phrases[phraseIndex].text} onscore={(score) => { repeatScores.push(score); repeatScored = true; }} />
      {/key}
      <div class="row">
        {#if repeatScored}<button class="btn btn-primary" onclick={nextPhrase}>{t('path.next')}</button>{/if}
        <button class="link-btn" onclick={nextPhrase}>{t('live.skip')}</button>
      </div>
    {:else if step === 2}
      <DialogueView lines={lesson.dialogue} />
      <button class="btn btn-primary" style="justify-self: start" onclick={next}>{t('path.next')}</button>
    {:else if step === 3}
      <QuizCard questions={lesson.quiz} onchecked={(score, total) => { quizScore = Math.round((score / total) * 100); }} />
      {#if quizScore !== null}<button class="btn btn-primary" style="justify-self: start" onclick={next}>{t('path.next')}</button>{/if}
    {:else}
      <article class="card stack">
        <h2>{t('path.score', { score: finalScore })}</h2>
        {#if lesson.tip}<p><strong>{t('path.tip')}.</strong> {lesson.tip}</p>{/if}
      </article>
      {#if errorCode}<ErrorNotice code={errorCode} />{/if}
      {#if !saved}
        <button class="btn btn-primary" style="justify-self: start" onclick={finish}>{t('path.finish')}</button>
      {:else}
        <div class="row">
          {#if nextUnit}<a class="btn btn-primary" href="/path/{nextUnit.id}" style="text-decoration: none">{t('path.nextlesson')}</a>{/if}
          <a class="btn" href="/path" style="text-decoration: none">{t('path.back')}</a>
        </div>
      {/if}
    {/if}
  {/if}
</section>

<style>
  .back { justify-self: start; }
  .steps { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 0.4rem; }
  .steps li { padding: 0.25rem 0.8rem; border-radius: 999px; background: var(--surface-2); color: var(--muted); font-size: 0.85rem; font-weight: 600; }
  .steps li.past { background: var(--accent-soft); color: var(--accent); }
  .steps li.on { background: var(--accent); color: var(--accent-ink); }
</style>
