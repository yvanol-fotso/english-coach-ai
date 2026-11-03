<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, speak } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { ReviewGrade, SavedWord } from '$lib/types';

  let { word, ongrade }: { word: SavedWord; ongrade: (grade: ReviewGrade) => void } = $props();

  let shown = $state(false);
  const grades: ReviewGrade[] = ['again', 'hard', 'good', 'easy'];
</script>

<article class="card stack">
  <div class="row">
    <h2 class="term">{word.term}</h2>
    {#if canSpeak()}
      <button class="link-btn" onclick={() => speak(word.term, { rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName })}>{t('common.listen')}</button>
    {/if}
  </div>
  {#if shown}
    <p class="translation">{word.translation}</p>
    <p>{word.definition}</p>
    {#if word.examples[0]}<p class="muted">{word.examples[0]}</p>{/if}
    <div class="row">
      {#each grades as grade}
        <button class="btn" class:btn-primary={grade === 'good'} onclick={() => ongrade(grade)}>{t(`review.${grade}`)}</button>
      {/each}
    </div>
  {:else}
    <button class="btn btn-primary" style="justify-self: start" onclick={() => (shown = true)}>{t('review.show')}</button>
  {/if}
</article>

<style>
  .term { font-size: 1.6rem; }
  .translation { font: 600 1.3rem var(--font-display); color: var(--accent); }
</style>
