<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';

  let { days }: { days: { day: string; count: number }[] } = $props();
</script>

<div class="strip" role="img" aria-label={t('progress.last28')}>
  {#each days as d}
    <span class="cell" class:on={d.count > 0} class:strong={d.count > 3} title="{d.day} : {d.count}"></span>
  {/each}
</div>

<style>
  .strip { display: grid; grid-template-columns: repeat(14, 1fr); gap: 0.35rem; }
  .cell { aspect-ratio: 1; border-radius: 6px; background: var(--surface-2); }
  .on { background: var(--accent-soft); outline: 1px solid var(--accent); }
  .strong { background: var(--accent); }
</style>
