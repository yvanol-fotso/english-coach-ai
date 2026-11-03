<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, speak } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { Explanation } from '$lib/types';

  let { word, saved, onsave }: { word: Explanation; saved: boolean; onsave: () => void } = $props();
</script>

<article class="card stack">
  <div class="head">
    <h2>{word.term}</h2>
    <span class="muted">{word.part_of_speech}</span>
  </div>
  <p class="translation">{word.translation}</p>
  <p>{word.definition}</p>
  {#if word.examples.length}
    <ul>{#each word.examples as example}<li>{example}</li>{/each}</ul>
  {/if}
  {#if word.pronunciation_tip}<p class="muted">{word.pronunciation_tip}</p>{/if}
  <div class="row">
    {#if canSpeak()}
      <button class="btn btn-sm" onclick={() => speak(word.term, { rate: settings.speechRate, server: settings.serverTts })}>{t('common.listen')}</button>
    {/if}
    <button class="btn btn-sm btn-primary" onclick={onsave} disabled={saved}>{saved ? t('vocab.saved') : t('vocab.add')}</button>
  </div>
</article>

<style>
  .head { display: flex; align-items: baseline; gap: 0.7rem; }
  .translation { font: 600 1.3rem var(--font-display); color: var(--accent); }
  ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 0.25rem; }
</style>
