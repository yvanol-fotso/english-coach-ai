<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
</script>

<svelte:head><title>{t('nav.studio')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('studio.title')}</h1>
    <p class="lead">{t('studio.lead')}</p>
  </div>

  {#if data.catalog === null}
    <ErrorNotice code="backend_unreachable" />
  {:else}
    <div class="grid">
      {#each data.catalog.tools as tool}
        <a class="card" href="/studio/{tool.id}">
          <span class="ico"><Icon name={tool.icon as 'feather'} size={20} /></span>
          <h2>{pick(tool.title)}</h2>
          <p class="muted">{pick(tool.description)}</p>
        </a>
      {/each}
    </div>
  {/if}
</section>

<style>
  .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); }
  .card { text-decoration: none; display: grid; gap: 0.4rem; align-content: start; }
  .card:hover { border-color: var(--accent); }
  .ico { display: grid; place-items: center; width: 2.4rem; height: 2.4rem; border-radius: 12px; background: var(--accent-soft); color: var(--accent); }
</style>
