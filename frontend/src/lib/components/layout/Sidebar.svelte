<script lang="ts">
  import { page } from '$app/state';
  import Icon from '$lib/components/ui/Icon.svelte';
  import Logo from '$lib/components/ui/Logo.svelte';
  import TargetSelect from '$lib/components/ui/TargetSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import type { CatalogLanguage, HealthStatus } from '$lib/types';
  import StatusBadge from './StatusBadge.svelte';

  let { health, profile, languages }: { health: HealthStatus; profile: string | null; languages: CatalogLanguage[] } = $props();

  const groups = [
    { key: 'nav.group.learn', links: [
      { href: '/path', key: 'nav.path', icon: 'route' },
      { href: '/chat', key: 'nav.talk', icon: 'chat' },
      { href: '/call', key: 'nav.call', icon: 'phone' },
      { href: '/ask', key: 'nav.ask', icon: 'question' }
    ] },
    { key: 'nav.group.practice', links: [
      { href: '/drills', key: 'nav.drills', icon: 'wave' },
      { href: '/correct', key: 'nav.write', icon: 'pencil' },
      { href: '/practice', key: 'nav.understand', icon: 'book' },
      { href: '/translate', key: 'nav.translate', icon: 'translate' },
      { href: '/studio', key: 'nav.studio', icon: 'grid' }
    ] },
    { key: 'nav.group.me', links: [
      { href: '/vocabulary', key: 'nav.vocabulary', icon: 'bookmark' },
      { href: '/history', key: 'nav.history', icon: 'clock' },
      { href: '/progress', key: 'nav.progress', icon: 'chart' }
    ] }
  ] as const;

  const isActive = (href: string) => (href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href));
</script>

<aside>
  <a class="brand" href="/"><Logo size={32} /> English Coach</a>
  <TargetSelect {languages} />
  <nav aria-label={t('nav.main')}>
    {#each groups as group}
      <p class="group">{t(group.key)}</p>
      {#each group.links as link}
        <a href={link.href} aria-current={isActive(link.href) ? 'page' : undefined}>
          <Icon name={link.icon} size={18} /><span>{t(link.key)}</span>
        </a>
      {/each}
    {/each}
    <a class="settings" href="/settings" aria-current={isActive('/settings') ? 'page' : undefined}>
      <Icon name="sliders" size={18} /><span>{profile ?? t('nav.settings')}</span>
    </a>
  </nav>
  <div class="foot"><StatusBadge {health} /></div>
</aside>

<style>
  aside { display: flex; flex-direction: column; gap: 1rem; padding: 1.2rem 1rem; background: var(--surface); border-right: 1px solid var(--line); height: 100dvh; position: sticky; top: 0; overflow-y: auto; }
  .brand { display: flex; align-items: center; gap: 0.6rem; font: 700 1.2rem var(--font-display); text-decoration: none; padding-inline: 0.5rem; }
  nav { display: grid; gap: 0.15rem; }
  .group { margin: 0.7rem 0 0.2rem; padding-inline: 0.75rem; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--muted); }
  nav a { display: flex; align-items: center; gap: 0.7rem; padding: 0.5rem 0.75rem; border-radius: 12px; text-decoration: none; color: var(--muted); font-weight: 550; }
  nav a:hover { background: var(--surface-2); color: var(--ink); }
  nav a[aria-current='page'] { background: var(--accent-soft); color: var(--accent); font-weight: 650; }
  .settings { margin-top: 0.8rem; border-top: 1px solid var(--line); border-radius: 0 0 12px 12px; padding-top: 0.9rem; }
  .foot { margin-top: auto; }

  @media (max-width: 760px) {
    aside { flex-direction: row; height: auto; position: static; border-right: 0; border-top: 1px solid var(--line); padding: 0.4rem; overflow: visible; }
    .brand, .foot, .group { display: none; }
    nav { display: flex; width: 100%; overflow-x: auto; gap: 0.1rem; }
    nav a { flex: 1 0 auto; flex-direction: column; gap: 0.1rem; font-size: 0.7rem; padding: 0.4rem 0.6rem; }
    .settings { margin: 0; border: 0; padding-top: 0.4rem; border-radius: 12px; }
  }
</style>
