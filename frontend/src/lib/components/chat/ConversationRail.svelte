<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import type { ConversationSummary } from '$lib/types';
  import { formatDay } from '$lib/utils/format';

  let { items, activeId, onnew }: { items: ConversationSummary[]; activeId: number | null; onnew: () => void } = $props();
</script>

<aside class="rail" aria-label={t('rail.title')}>
  <div class="head">
    <h2>{t('rail.title')}</h2>
    <button class="btn btn-sm" onclick={onnew}>{t('rail.new')}</button>
  </div>
  {#if items.length === 0}
    <p class="muted">{t('rail.empty')}</p>
  {:else}
    <ul>
      {#each items as item (item.id)}
        <li>
          <a href="/chat?c={item.id}" aria-current={item.id === activeId ? 'true' : undefined}>
            <span class="title">{item.title}</span>
            <span class="muted">{formatDay(item.updated_at)}</span>
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</aside>

<style>
  .rail { display: none; flex-direction: column; gap: 0.8rem; width: 15rem; flex: none; padding: 1.25rem 0.9rem; border-right: 1px solid var(--line); overflow-y: auto; }
  .head { display: flex; align-items: center; justify-content: space-between; }
  ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.2rem; }
  a { display: grid; padding: 0.5rem 0.65rem; border-radius: var(--radius-sm); text-decoration: none; font-size: 0.92rem; }
  a:hover { background: var(--surface-2); }
  a[aria-current='true'] { background: var(--accent-soft); color: var(--accent); }
  .title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 550; }
  .muted { font-size: 0.8rem; }
  @media (min-width: 1100px) { .rail { display: flex; } }
</style>
