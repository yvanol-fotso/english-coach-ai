<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, speak, speakSequence } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { Phrase } from '$lib/types';

  let { phrases }: { phrases: Phrase[] } = $props();

  const options = () => ({ rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName });
</script>

{#if canSpeak()}
  <button class="btn btn-sm" style="justify-self: start" onclick={() => speakSequence(phrases.map((p) => p.text), options())}>{t('path.listenall')}</button>
{/if}
<ul class="phrases">
  {#each phrases as phrase}
    <li class="card">
      <div class="text">
        <strong class="target">{phrase.text}</strong>
        <span>{phrase.meaning}</span>
        {#if phrase.tip}<span class="muted tip">{phrase.tip}</span>{/if}
      </div>
      {#if canSpeak()}<button class="btn btn-sm" onclick={() => speak(phrase.text, options())}>{t('common.listen')}</button>{/if}
    </li>
  {/each}
</ul>

<style>
  .phrases { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.5rem; }
  li { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.8rem 1rem; }
  .text { display: grid; }
  .target { font: 650 1.2rem var(--font-display); }
  .tip { font-size: 0.85rem; }
</style>
