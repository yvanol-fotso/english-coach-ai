<script lang="ts">
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import type { CorrectionResult } from '$lib/types';
  import { sameText } from '$lib/utils/diff';

  let { correction, original }: { correction: CorrectionResult; original: string } = $props();

  const unchanged = $derived(sameText(correction.corrected_text, original));
</script>

{#if correction.issues.length}
  <div class="fix">
    <p><span class="label">{t('fix.better')}</span> {correction.corrected_text}</p>
    <ul>
      {#each correction.issues as issue}
        <li><del>{issue.original}</del> → <strong>{issue.correction}</strong> <span class="muted">· {issue.explanation}</span></li>
      {/each}
    </ul>
  </div>
{:else if !unchanged}
  <div class="fix"><p><span class="label">{t('fix.english')}</span> {correction.corrected_text}</p></div>
{:else}
  <p class="ok muted"><Icon name="check" size={14} /> {t('fix.ok')}</p>
{/if}

<style>
  .fix { display: grid; gap: 0.4rem; padding: 0.6rem 0.85rem; border-radius: var(--radius-sm); background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--accent); font-size: 0.93rem; text-align: left; }
  .label { font-weight: 700; color: var(--accent); margin-right: 0.3rem; }
  ul { margin: 0; padding-left: 1.1rem; display: grid; gap: 0.2rem; }
  del { color: var(--bad); }
  .ok { display: flex; align-items: center; gap: 0.3rem; font-size: 0.85rem; }
</style>
