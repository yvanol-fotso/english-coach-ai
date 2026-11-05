<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import LanguagePicker from '$lib/components/ui/LanguagePicker.svelte';
  import { FALLBACK_LANGUAGES } from '$lib/data/languages';
  import { t } from '$lib/i18n/index.svelte';
  import { pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  const units = $derived(data.catalog?.units ?? []);
  const state = $derived(new Map((data.progress ?? []).map((p) => [p.id, p])));
  const nextId = $derived(units.find((u) => !state.get(u.id)?.done)?.id);
</script>

<svelte:head><title>{t('nav.path')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('path.title')}</h1>
    <p class="lead">{t('path.lead')}</p>
  </div>

  <LanguagePicker languages={data.catalog?.languages ?? FALLBACK_LANGUAGES} />

  {#if data.catalog === null}
    <ErrorNotice code="backend_unreachable" />
  {:else}
    <ol class="units">
      {#each units as unit, i (unit.id)}
        {@const done = state.get(unit.id)}
        <li>
          <a class="card unit" class:next={unit.id === nextId} href="/path/{unit.id}">
            <span class="num" class:done={done?.done}>{done?.done ? '✓' : i + 1}</span>
            <span class="text">
              <strong>{pick(unit.title)}</strong>
              <span class="muted">{pick(unit.goal)}</span>
            </span>
            <span class="side muted">
              {#if done?.done}{done.score} %{:else if unit.id === nextId}<b class="go">{t('path.start')}</b>{:else}{t('path.level', { level: unit.level })}{/if}
            </span>
          </a>
        </li>
      {/each}
    </ol>
  {/if}
</section>

<style>
  .units { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.6rem; }
  .unit { display: flex; align-items: center; gap: 1rem; text-decoration: none; }
  .unit:hover, .unit.next { border-color: var(--accent); }
  .num { display: grid; place-items: center; width: 2.4rem; height: 2.4rem; border-radius: 50%; background: var(--surface-2); font: 700 1rem var(--font-display); flex: none; }
  .num.done { background: var(--accent); color: var(--accent-ink); }
  .text { display: grid; flex: 1; min-width: 0; }
  .side { font-size: 0.88rem; white-space: nowrap; }
  .go { color: var(--accent); font-size: 0.95rem; }
</style>
