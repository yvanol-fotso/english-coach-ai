<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import { canSpeak, stopSpeaking } from '$lib/services/speech';
  import type { AnswerMode } from '$lib/stores/settings.svelte';
  import type { QuickAnswer } from '$lib/types';

  let { question, answer, mode, onplay }: { question: string; answer: QuickAnswer; mode: AnswerMode; onplay: () => void } = $props();

  let revealed = $state(false);
  const showText = $derived(mode !== 'voice' || revealed);
</script>

<article class="card stack">
  <p class="muted q">{question}</p>
  <div class="row head">
    <h2>{answer.title}</h2>
    {#if canSpeak()}
      <button class="btn btn-sm btn-primary" onclick={onplay}>{t('ask.listen')}</button>
      <button class="link-btn" onclick={stopSpeaking}>{t('common.stop')}</button>
    {/if}
    {#if mode === 'voice'}
      <button class="link-btn" onclick={() => (revealed = !revealed)}>{revealed ? t('ask.hide') : t('ask.show')}</button>
    {/if}
  </div>

  {#if showText}
    <section class="block"><h3>{t('ask.rule')}</h3><p>{answer.rule}</p></section>
    {#if answer.examples.length}
      <section class="block"><h3>{t('ask.examples')}</h3><ul>{#each answer.examples as example}<li>{example}</li>{/each}</ul></section>
    {/if}
    {#if answer.exceptions.length}
      <section class="block"><h3>{t('ask.exceptions')}</h3><ul>{#each answer.exceptions as exception}<li>{exception}</li>{/each}</ul></section>
    {/if}
    {#if answer.watch_out}<p class="notice notice-warn"><strong>{t('ask.watch')}.</strong> {answer.watch_out}</p>{/if}
  {/if}
</article>

<style>
  .q { font-size: 0.9rem; }
  .head { gap: 0.8rem; }
  .block { display: grid; gap: 0.3rem; }
  h3 { font: 700 0.8rem var(--font); text-transform: uppercase; letter-spacing: 0.06em; color: var(--accent); }
  ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 0.25rem; }
</style>
