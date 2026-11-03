<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, speak, type SpeechLang } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { TranslationResult } from '$lib/types';

  let { result }: { result: TranslationResult } = $props();
  let copied = $state(false);

  const lang = $derived<SpeechLang>(result.target_language === 'en' ? 'en-US' : 'fr-FR');

  async function copy() {
    await navigator.clipboard.writeText(result.translation);
    copied = true;
    setTimeout(() => (copied = false), 1500);
  }
</script>

<article class="card stack">
  <p class="muted">{t('translate.direction', { from: t(`lang.${result.source_language}`), to: t(`lang.${result.target_language}`) })}</p>
  <p class="main">{result.translation}</p>
  <div class="row">
    <button class="btn btn-sm" onclick={copy}>{copied ? t('common.copied') : t('common.copy')}</button>
    {#if canSpeak()}
      <button class="btn btn-sm" onclick={() => speak(result.translation, { rate: settings.speechRate, lang, server: settings.serverTts })}>{t('common.listen')}</button>
    {/if}
  </div>
  {#if result.alternatives.length}
    <div class="stack">
      <h2>{t('translate.alternatives')}</h2>
      <ul>{#each result.alternatives as alt}<li>{alt}</li>{/each}</ul>
    </div>
  {/if}
</article>

<style>
  .main { font-size: 1.25rem; white-space: pre-wrap; }
  ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 0.3rem; }
</style>
