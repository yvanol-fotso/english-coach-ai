<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import type { CallSummary } from '$lib/types';

  let { summary, time }: { summary: CallSummary; time: string } = $props();
</script>

<article class="card stack">
  <h2>{t('call.summary')}</h2>
  <p class="muted">{t('call.duration', { time })}</p>
  <p>{summary.summary}</p>

  {#if summary.mistakes.length}
    <div class="stack">
      <h2>{t('call.mistakes')}</h2>
      <ul class="issues">
        {#each summary.mistakes as m}
          <li><p><del>{m.wrong}</del> → <strong>{m.right}</strong></p><p class="muted">{m.why}</p></li>
        {/each}
      </ul>
    </div>
  {/if}

  {#if summary.phrases.length}
    <div class="stack">
      <h2>{t('call.phrases')}</h2>
      <ul>{#each summary.phrases as phrase}<li>{phrase}</li>{/each}</ul>
    </div>
  {/if}

  <p class="next"><strong>{t('call.next')}.</strong> {summary.next_step}</p>
</article>

<style>
  ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 0.3rem; }
  .issues { list-style: none; padding: 0; gap: 0.75rem; }
  .issues li { border-left: 3px solid var(--accent); padding-left: 0.75rem; }
  del { color: var(--bad); }
  .next { background: var(--surface-2); padding: 0.6rem 0.8rem; border-radius: var(--radius-sm); }
</style>
