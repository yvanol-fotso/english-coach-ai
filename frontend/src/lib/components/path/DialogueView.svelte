<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, speak, speakSequence } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { Lesson } from '$lib/types';

  let { lines }: { lines: Lesson['dialogue'] } = $props();
  let meanings = $state(true);

  const options = () => ({ rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName });
</script>

<div class="row">
  {#if canSpeak()}<button class="btn btn-sm" onclick={() => speakSequence(lines.map((l) => l.text), options())}>{t('path.listenall')}</button>{/if}
  <label class="toggle"><input type="checkbox" bind:checked={meanings} /> {t('path.meaning')}</label>
</div>
<div class="dialogue">
  {#each lines as line, i}
    <div class="turn" class:right={line.speaker.trim().toUpperCase() !== 'A'}>
      <button class="bubble" onclick={() => speak(line.text, options())} aria-label={t('common.listen')}>
        <span class="who muted">{line.speaker}</span>
        <strong>{line.text}</strong>
        {#if meanings}<span class="muted">{line.meaning}</span>{/if}
      </button>
    </div>
  {/each}
</div>

<style>
  .dialogue { display: grid; gap: 0.7rem; }
  .turn { display: flex; }
  .turn.right { justify-content: flex-end; }
  .bubble { display: grid; gap: 0.15rem; text-align: left; max-width: min(28rem, 90%); padding: 0.7rem 1rem; border: 1px solid var(--line); border-radius: 16px 16px 16px 4px; background: var(--surface); color: var(--ink); font: inherit; cursor: pointer; }
  .right .bubble { border-radius: 16px 16px 4px 16px; background: var(--accent-soft); border-color: var(--accent); }
  .who { font-size: 0.75rem; font-weight: 700; }
  .toggle { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--muted); cursor: pointer; }
</style>
