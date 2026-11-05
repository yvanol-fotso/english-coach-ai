<script lang="ts">
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';

  let {
    phase,
    heard,
    langLabel,
    onlang,
    onskip,
    onend
  }: { phase: 'listening' | 'thinking' | 'speaking' | 'muted'; heard: string; langLabel: string; onlang: () => void; onskip: () => void; onend: () => void } = $props();
</script>

<div class="live card">
  <div class="orb {phase}"><Icon name={phase === 'speaking' ? 'wave' : 'mic'} size={28} /></div>
  <div class="info">
    <strong role="status">{t(`live.${phase}`)}</strong>
    <p class="muted heard">{phase === 'listening' && heard ? heard : t('live.hint')}</p>
  </div>
  <div class="row">
    <button class="link-btn" onclick={onlang}>{langLabel}</button>
    {#if phase === 'speaking'}<button class="btn btn-sm" onclick={onskip}>{t('live.skip')}</button>{/if}
    <button class="btn btn-sm" onclick={onend}>{t('live.end')}</button>
  </div>
</div>

<style>
  .live { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
  .info { flex: 1; min-width: 10rem; display: grid; }
  .heard { font-size: 0.92rem; }
  .orb { width: 3.6rem; height: 3.6rem; border-radius: 50%; display: grid; place-items: center; flex: none; background: var(--accent-soft); color: var(--accent); }
  .listening { background: var(--hl); color: var(--hl-ink); animation: pulse 1.4s ease-out infinite; }
  .speaking { background: var(--accent); color: var(--accent-ink); animation: pulse 1.2s ease-out infinite; }
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--accent) 45%, transparent); }
    100% { box-shadow: 0 0 0 16px transparent; }
  }
</style>
