<script lang="ts">
  import { page } from '$app/state';
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import type { HealthStatus } from '$lib/types';
  import StatusBadge from './StatusBadge.svelte';

  let { health, profile }: { health: HealthStatus; profile: string | null } = $props();

  const links = [
    { href: '/', key: 'nav.home', icon: 'home' },
    { href: '/chat', key: 'nav.talk', icon: 'chat' },
    { href: '/drills', key: 'nav.drills', icon: 'wave' },
    { href: '/correct', key: 'nav.write', icon: 'pencil' },
    { href: '/practice', key: 'nav.understand', icon: 'book' },
    { href: '/translate', key: 'nav.translate', icon: 'translate' },
    { href: '/studio', key: 'nav.studio', icon: 'grid' },
    { href: '/vocabulary', key: 'nav.vocabulary', icon: 'bookmark' },
    { href: '/history', key: 'nav.history', icon: 'clock' },
    { href: '/progress', key: 'nav.progress', icon: 'chart' }
  ] as const;

  const isActive = (href: string) => (href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href));
</script>

<aside>
  <a class="brand" href="/">
    <span class="mark"><Icon name="chat" size={18} /></span>
    English Coach
  </a>
  <nav aria-label={t('nav.main')}>
    {#each links as link}
      <a href={link.href} aria-current={isActive(link.href) ? 'page' : undefined}>
        <Icon name={link.icon} size={18} /><span>{t(link.key)}</span>
      </a>
    {/each}
    <a class="settings" href="/settings" aria-current={isActive('/settings') ? 'page' : undefined}>
      <Icon name="sliders" size={18} /><span>{profile ?? t('nav.settings')}</span>
    </a>
  </nav>
  <div class="foot"><StatusBadge {health} /></div>
</aside>

<style>
  aside { display: flex; flex-direction: column; gap: 1.5rem; padding: 1.4rem 1rem; background: var(--surface); border-right: 1px solid var(--line); height: 100dvh; position: sticky; top: 0; }
  .brand { display: flex; align-items: center; gap: 0.6rem; font: 700 1.2rem var(--font-display); text-decoration: none; padding-inline: 0.5rem; }
  .mark { display: grid; place-items: center; width: 2rem; height: 2rem; border-radius: 10px; background: var(--accent); color: var(--accent-ink); }
  nav { display: grid; gap: 0.2rem; }
  nav a { display: flex; align-items: center; gap: 0.7rem; padding: 0.6rem 0.75rem; border-radius: 12px; text-decoration: none; color: var(--muted); font-weight: 550; }
  nav a:hover { background: var(--surface-2); color: var(--ink); }
  nav a[aria-current='page'] { background: var(--accent-soft); color: var(--accent); font-weight: 650; }
  .settings { margin-top: 0.8rem; border-top: 1px solid var(--line); border-radius: 0 0 12px 12px; padding-top: 1rem; }
  .foot { margin-top: auto; }

  @media (max-width: 760px) {
    aside { flex-direction: row; height: auto; position: static; border-right: 0; border-top: 1px solid var(--line); padding: 0.4rem; }
    .brand, .foot { display: none; }
    nav { display: flex; width: 100%; overflow-x: auto; gap: 0.1rem; }
    nav a { flex: 1 0 auto; flex-direction: column; gap: 0.1rem; font-size: 0.7rem; padding: 0.4rem 0.6rem; }
    .settings { margin: 0; border: 0; padding-top: 0.4rem; border-radius: 12px; }
  }
</style>
