<script lang="ts">
  import DictationCard from '$lib/components/practice/DictationCard.svelte';
  import PronunciationCard from '$lib/components/practice/PronunciationCard.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, generateDrill, logActivity } from '$lib/services/api';
  import { stopSpeaking } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';

  type Kind = 'pronunciation' | 'dictation';

  let kind = $state<Kind>('pronunciation');
  let topic = $state('');
  let sentences = $state<string[] | null>(null);
  let runKind = $state<Kind>('pronunciation');
  let index = $state(0);
  let scores = $state<number[]>([]);
  let scored = $state(false);
  let finished = $state(false);
  let loading = $state(false);
  let errorCode = $state('');

  const average = $derived(scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0);

  async function start() {
    loading = true;
    errorCode = '';
    stopSpeaking();
    try {
      const set = await generateDrill(kind, settings.level, topic.trim());
      sentences = set.sentences;
      runKind = kind;
      index = 0;
      scores = [];
      scored = false;
      finished = false;
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }

  const onscore = (score: number) => {
    scores.push(score);
    scored = true;
  };

  function next() {
    if (!sentences) return;
    if (index + 1 < sentences.length) {
      index++;
      scored = false;
      return;
    }
    finished = true;
    logActivity(runKind === 'pronunciation' ? 'pronunciation' : 'listening', average, { title: runKind, count: scores.length }).catch(() => {});
  }
</script>

<svelte:head><title>{t('nav.drills')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('drills.title')}</h1>
    <p class="lead">{t('drills.lead')}</p>
  </div>

  <div class="row">
    <div class="seg" role="group" aria-label={t('drills.title')}>
      <button aria-pressed={kind === 'pronunciation'} onclick={() => (kind = 'pronunciation')}>{t('drills.pron')}</button>
      <button aria-pressed={kind === 'dictation'} onclick={() => (kind = 'dictation')}>{t('drills.dict')}</button>
    </div>
    <LevelSelect />
  </div>
  <div class="row">
    <input class="field topic" bind:value={topic} placeholder={t('drills.topic')} maxlength="120" />
    <button class="btn btn-primary" onclick={start} disabled={loading}>{loading ? t('drills.loading') : sentences ? t('drills.again') : t('drills.start')}</button>
  </div>

  {#if errorCode}<ErrorNotice code={errorCode} onretry={start} />{/if}

  {#if sentences && !finished}
    <p class="muted">{t('drills.progress', { i: index + 1, n: sentences.length })}</p>
    {#key `${runKind}-${index}-${sentences[index]}`}
      {#if runKind === 'pronunciation'}
        <PronunciationCard sentence={sentences[index]} {onscore} />
      {:else}
        <DictationCard sentence={sentences[index]} {onscore} />
      {/if}
    {/key}
    {#if scored}
      <button class="btn btn-primary" style="justify-self: start" onclick={next}>
        {index + 1 < sentences.length ? t('drills.next') : t('drills.finish')}
      </button>
    {/if}
  {:else if finished}
    <article class="card stack"><h2>{t('drills.done', { score: average })}</h2></article>
  {/if}
</section>

<style>
  .topic { flex: 1; min-width: 10rem; width: auto; }
</style>
