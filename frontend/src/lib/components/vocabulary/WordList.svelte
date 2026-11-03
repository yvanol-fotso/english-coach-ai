<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, speak } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { SavedWord } from '$lib/types';

  let { words, onremove }: { words: SavedWord[]; onremove: (id: number) => void } = $props();
</script>

<ul class="list">
  {#each words as word (word.id)}
    <li class="card">
      <div>
        <strong>{word.term}</strong>
        <span class="muted"> · {word.translation}</span>
      </div>
      <div class="row">
        {#if canSpeak()}
          <button class="link-btn" onclick={() => speak(word.term, { rate: settings.speechRate, server: settings.serverTts })}>{t('common.listen')}</button>
        {/if}
        <button class="link-btn" onclick={() => onremove(word.id)}>{t('vocab.remove')}</button>
      </div>
    </li>
  {/each}
</ul>

<style>
  .list { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.5rem; }
  li { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 0.7rem 1rem; }
</style>
