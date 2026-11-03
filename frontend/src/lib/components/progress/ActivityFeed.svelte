<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import type { ActivityOut } from '$lib/types';
  import { formatDate } from '$lib/utils/format';

  let { items }: { items: ActivityOut[] } = $props();

  const text = (value: unknown) => String(value ?? '').slice(0, 90);

  function summary(activity: ActivityOut): string {
    const payload = activity.payload ?? {};
    switch (activity.skill) {
      case 'writing':
      case 'translation':
        return text(payload.original);
      case 'vocabulary':
        return text(payload.term);
      case 'speaking':
        return text(payload.title);
      default:
        return `${text(payload.title)}${activity.score != null ? ` · ${activity.score} %` : ''}`;
    }
  }
</script>

<ul class="feed">
  {#each items as item (item.id)}
    <li>
      <span class="skill">{t(`skill.${item.skill}`)}</span>
      <span class="summary">{summary(item)}</span>
      <time class="muted" datetime={item.created_at}>{formatDate(item.created_at)}</time>
    </li>
  {/each}
</ul>

<style>
  .feed { list-style: none; margin: 0; padding: 0; display: grid; }
  li { display: grid; grid-template-columns: 10rem 1fr auto; gap: 0.8rem; padding: 0.6rem 0; border-top: 1px solid var(--line); align-items: baseline; }
  li:first-child { border-top: 0; }
  .skill { font-weight: 600; color: var(--accent); }
  .summary { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  time { font-size: 0.85rem; }
  @media (max-width: 640px) { li { grid-template-columns: 1fr auto; } .summary { grid-column: 1 / -1; order: 3; } }
</style>
