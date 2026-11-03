<script lang="ts">
  import ActivityFeed from '$lib/components/progress/ActivityFeed.svelte';
  import ActivityStrip from '$lib/components/progress/ActivityStrip.svelte';
  import SkillBars from '$lib/components/progress/SkillBars.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import { plural, t } from '$lib/i18n/index.svelte';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
</script>

<svelte:head><title>{t('nav.progress')} · English Coach</title></svelte:head>

<section class="page">
  {#if data.stats === null}
    <h1>{t('progress.title')}</h1>
    <ErrorNotice code="backend_unreachable" />
  {:else}
    <div class="page-head">
      <h1>{t('progress.title')}</h1>
      <p class="lead">
        {data.stats.streak > 0 ? plural('home.streak', data.stats.streak) : t('progress.streak.none')}
        {#if data.stats.total > 0} · {t('progress.total', { n: data.stats.total })}{/if}
      </p>
    </div>

    <div class="card stack">
      <h2>{t('progress.last28')}</h2>
      <ActivityStrip days={data.stats.days} />
    </div>

    <div class="card stack">
      <h2>{t('progress.skills')}</h2>
      <SkillBars counts={data.stats.by_skill} />
    </div>

    <div class="card stack">
      <h2>{t('progress.recent')}</h2>
      {#if data.activities.length}
        <ActivityFeed items={data.activities} />
      {:else}
        <p class="muted">{t('progress.empty')}</p>
      {/if}
    </div>
  {/if}
</section>
