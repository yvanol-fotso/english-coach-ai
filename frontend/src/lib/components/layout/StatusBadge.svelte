<script lang="ts">
  import { invalidate } from '$app/navigation';
  import { t } from '$lib/i18n/index.svelte';
  import type { HealthStatus } from '$lib/types';

  let { health }: { health: HealthStatus } = $props();

  const state = $derived(!health.api || !health.ollama ? 'bad' : !health.model_ready ? 'warn' : 'ok');
  const label = $derived(
    !health.api ? t('status.api') : !health.ollama ? t('status.ollama') : !health.model_ready ? t('status.model') : t('status.ready', { model: health.model })
  );
</script>

<button class="badge {state}" onclick={() => invalidate('app:health')} title={t('status.recheck')}>
  <span class="dot"></span>{label}
</button>

<style>
  .badge { display: flex; align-items: center; gap: 0.55rem; width: 100%; font: inherit; font-size: 0.85rem; padding: 0.5rem 0.75rem; border: 1px solid var(--line); border-radius: var(--radius-sm); background: var(--surface); color: var(--ink); cursor: pointer; text-align: left; }
  .dot { width: 0.6rem; height: 0.6rem; border-radius: 50%; background: currentColor; flex: none; }
  .ok .dot { color: var(--ok); }
  .warn .dot { color: var(--hl); }
  .bad .dot { color: var(--bad); }
</style>
