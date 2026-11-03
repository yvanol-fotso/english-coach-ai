<script lang="ts">
  import { onMount } from 'svelte';
  import DiffText from '$lib/components/practice/DiffText.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { speak } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import { compare, type DiffWord } from '$lib/utils/diff';

  let { sentence, onscore }: { sentence: string; onscore: (score: number) => void } = $props();

  let typed = $state('');
  let result = $state<{ words: DiffWord[]; score: number } | null>(null);

  const play = (rate = settings.speechRate) => speak(sentence, { rate, server: settings.serverTts, voice: settings.voiceName });

  function check() {
    result = compare(sentence, typed);
    onscore(result.score);
  }

  onMount(() => void play());
</script>

<article class="card stack">
  <p class="muted">{t('drills.hear')}</p>
  <div class="row">
    <button class="btn btn-primary" onclick={() => play()}>{t('drills.play')}</button>
    <button class="btn" onclick={() => play(0.65)}>0.65×</button>
  </div>
  <textarea class="field" rows="2" bind:value={typed} placeholder={t('drills.type')} disabled={!!result}></textarea>
  {#if result}
    <DiffText words={result.words} />
    <p><strong>{t('drills.score', { score: result.score })}</strong></p>
    <p class="muted">{sentence}</p>
  {:else}
    <button class="btn btn-primary" style="justify-self: start" onclick={check} disabled={!typed.trim()}>{t('drills.check')}</button>
  {/if}
</article>
