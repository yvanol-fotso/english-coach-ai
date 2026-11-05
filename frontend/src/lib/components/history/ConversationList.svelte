<script lang="ts">
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import type { ConversationSummary } from '$lib/types';
  import { formatDate, langName } from '$lib/utils/format';

  let { items, labelOf, ondelete }: { items: ConversationSummary[]; labelOf: (scenario: string) => string; ondelete: (id: number) => void } = $props();
</script>

<ul class="list">
  {#each items as item (item.id)}
    <li class="card">
      <a href="/chat?c={item.id}" class="main">
        <strong>{item.title}</strong>
        <span class="muted">
          {formatDate(item.updated_at)} · {t('history.messages', { n: item.message_count })} · {item.level} · {langName(item.language)}
          {#if item.scenario !== 'free'} · {labelOf(item.scenario)}{/if}
        </span>
      </a>
      <button class="icon" aria-label={t('common.delete')} title={t('common.delete')} onclick={() => ondelete(item.id)}>
        <Icon name="trash" size={18} />
      </button>
    </li>
  {/each}
</ul>

<style>
  .list { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.5rem; }
  li { display: flex; align-items: center; gap: 0.75rem; padding: 0; }
  li:hover { border-color: var(--accent); }
  .main { flex: 1; min-width: 0; display: grid; padding: 0.8rem 1rem; text-decoration: none; }
  .main strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .main span { font-size: 0.88rem; }
  .icon { border: 0; background: none; color: var(--muted); padding: 0.8rem 1rem; cursor: pointer; border-radius: var(--radius); }
  .icon:hover { color: var(--bad); }
</style>
