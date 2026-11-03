<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import type { CorrectionResult } from '$lib/types';

  let { result }: { result: CorrectionResult } = $props();
</script>

<article class="card stack">
  <h2>{t('write.result')}</h2>
  <p class="fixed">{result.corrected_text}</p>

  {#if result.issues.length === 0}
    <p class="muted">{t('write.none')}</p>
  {:else}
    <ul class="issues">
      {#each result.issues as issue}
        <li>
          <p><del>{issue.original}</del> → <strong>{issue.correction}</strong></p>
          <p class="muted">{issue.explanation}</p>
        </li>
      {/each}
    </ul>
  {/if}

  {#if result.tip}<p class="tip"><strong>{t('write.tip')}.</strong> {result.tip}</p>{/if}
</article>

<style>
  .fixed { white-space: pre-wrap; font-size: 1.1rem; }
  .issues { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.75rem; }
  .issues li { border-left: 3px solid var(--accent); padding-left: 0.75rem; }
  del { color: var(--bad); }
  .tip { background: var(--surface-2); padding: 0.6rem 0.8rem; border-radius: var(--radius-sm); }
</style>
