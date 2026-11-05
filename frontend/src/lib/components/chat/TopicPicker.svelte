<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import type { Catalog } from '$lib/types';
  import { pick } from '$lib/utils/format';

  const line = (starters: Record<string, string>) => starters[preferences.target] ?? starters.en;

  let {
    catalog,
    scenario,
    onstart,
    onscenario
  }: { catalog: Catalog | null; scenario: string; onstart: (text: string) => void; onscenario: (id: string) => void } = $props();
</script>

<div class="picker">
  <div class="stack intro">
    <h1>{t('talk.ask')}</h1>
    <p class="lead">{t('talk.lead')}</p>
  </div>

  {#if catalog === null}
    <ErrorNotice code="backend_unreachable" />
  {:else}
    <div class="stack">
      <h2>{t('talk.topics')}</h2>
      <div class="row">
        {#each catalog.topics as topic}
          <button class="chip" onclick={() => onstart(line(topic.starter))}>{pick(topic.label)}</button>
        {/each}
      </div>
    </div>

    <div class="stack">
      <h2>{t('talk.situations')}</h2>
      <div class="row">
        {#each catalog.scenarios.filter((s) => s.chip) as situation}
          <button class="chip" aria-pressed={scenario === situation.id} onclick={() => { onscenario(situation.id); onstart(line(situation.starter)); }}>
            {pick(situation.label)}
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <p class="muted">{t('talk.or')}</p>
</div>

<style>
  .picker { flex: 1; display: grid; align-content: center; gap: 1.5rem; }
  .intro { gap: 0.5rem; }
</style>
