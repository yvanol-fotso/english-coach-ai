<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import { plural, t } from '$lib/i18n/index.svelte';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  const cards = [
    { href: '/chat', icon: 'chat', title: 'nav.talk', text: 'home.talk' },
    { href: '/drills', icon: 'wave', title: 'nav.drills', text: 'home.drills' },
    { href: '/correct', icon: 'pencil', title: 'nav.write', text: 'home.write' },
    { href: '/practice', icon: 'book', title: 'nav.understand', text: 'home.understand' },
    { href: '/studio', icon: 'grid', title: 'nav.studio', text: 'home.studio' },
    { href: '/translate', icon: 'translate', title: 'nav.translate', text: 'home.translate' }
  ] as const;

  const setup = $derived(
    !data.health.api ? 'backend_unreachable' : !data.health.ollama ? 'llm_unavailable' : !data.health.model_ready ? 'model_missing' : ''
  );
</script>

<svelte:head><title>English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{data.profile ? t('home.title', { name: data.profile }) : t('home.title.anon')}</h1>
    <p class="lead">
      {t('home.lead')}
      {#if data.stats && data.stats.streak > 0}<span class="streak">{plural('home.streak', data.stats.streak)}</span>{/if}
    </p>
  </div>

  {#if setup}<ErrorNotice code={setup} model={data.health.model} />{/if}

  <a class="cta" href="/chat"><Icon name="mic" size={22} /> {t('live.start')}</a>

  <div class="grid">
    {#each cards as card}
      <a class="card" href={card.href}>
        <span class="ico"><Icon name={card.icon} size={20} /></span>
        <h2>{t(card.title)}</h2>
        <p class="muted">{t(card.text)}</p>
      </a>
    {/each}
  </div>
</section>

<style>
  .streak { display: inline-block; margin-left: 0.4rem; padding: 0.1rem 0.7rem; border-radius: 999px; background: var(--hl-soft); border: 1px solid var(--hl); color: var(--ink); font-size: 0.9rem; font-weight: 600; }
  .cta { justify-self: start; display: inline-flex; align-items: center; gap: 0.7rem; padding: 0.9rem 1.5rem; border-radius: 999px; background: var(--hl); color: var(--hl-ink); font: 700 1.05rem var(--font-display); text-decoration: none; }
  .cta:hover { filter: brightness(1.05); }
  .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); }
  .card { text-decoration: none; display: grid; gap: 0.4rem; align-content: start; }
  .card:hover { border-color: var(--accent); }
  .ico { display: grid; place-items: center; width: 2.4rem; height: 2.4rem; border-radius: 12px; background: var(--accent-soft); color: var(--accent); }
</style>
