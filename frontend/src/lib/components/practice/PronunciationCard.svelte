<script lang="ts">
  import DiffText from '$lib/components/practice/DiffText.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { canDictate, dictate, speak, type DictationStatus } from '$lib/services/speech';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { settings } from '$lib/stores/settings.svelte';
  import { compare, type DiffWord } from '$lib/utils/diff';

  let { sentence, onscore }: { sentence: string; onscore: (score: number) => void } = $props();

  let status = $state<DictationStatus>('idle');
  let heard = $state('');
  let result = $state<{ words: DiffWord[]; score: number } | null>(null);
  let stopDictation: (() => void) | null = null;

  const play = () => speak(sentence, { rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName });

  function record() {
    if (status === 'listening') return stopDictation?.();
    result = null;
    stopDictation = dictate({
      lang: preferences.locale,
      server: settings.serverStt,
      autoStop: true,
      onText: (text) => (heard = text),
      onFinal: (text) => {
        heard = text;
        result = compare(sentence, text);
        onscore(result.score);
      },
      onStatus: (s) => (status = s)
    });
  }
</script>

<article class="card stack">
  <p class="muted">{t('drills.say')}</p>
  <p class="target">{sentence}</p>
  <div class="row">
    <button class="btn" onclick={play}>{t('drills.play')}</button>
    {#if canDictate(settings.serverStt)}
      <button class="btn btn-primary" onclick={record} disabled={status === 'processing'}>
        <Icon name="mic" size={18} />
        {status === 'listening' ? t('drills.recording') : status === 'processing' ? t('drills.processing') : t('drills.record')}
      </button>
    {:else}
      <span class="muted">{t('drills.nomic')}</span>
    {/if}
  </div>

  {#if result}
    <DiffText words={result.words} />
    <p><strong>{t('drills.score', { score: result.score })}</strong></p>
    <p class="muted">{t('drills.heard', { text: heard })}</p>
    <p class="muted legend">{t('drills.legend')}</p>
  {/if}
</article>

<style>
  .target { font: 600 1.35rem var(--font-display); }
  .legend { font-size: 0.85rem; }
</style>
