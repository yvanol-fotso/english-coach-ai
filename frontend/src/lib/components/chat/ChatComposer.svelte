<script lang="ts">
  import { autoresize } from '$lib/actions/autoresize';
  import Icon from '$lib/components/ui/Icon.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { canDictate, dictate, type DictationStatus } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';

  let { busy, lang, langLabel, onlang, onsend, onstop }: { busy: boolean; lang: string; langLabel: string; onlang: () => void; onsend: (text: string) => void; onstop: () => void } = $props();

  let text = $state('');
  let status = $state<DictationStatus>('idle');
  let stopDictation: (() => void) | null = null;

  const hint = $derived(status === 'listening' ? t('mic.listening') : status === 'processing' ? t('mic.processing') : '');

  function submit() {
    const value = text.trim();
    if (!value || busy) return;
    onsend(value);
    text = '';
  }

  function toggleMic() {
    if (status === 'listening') return stopDictation?.();
    stopDictation = dictate({ lang, server: settings.serverStt, onText: (heard) => (text = heard), onStatus: (s) => (status = s) });
  }

  function onkeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  }
</script>

<div class="composer">
  {#if hint}<p class="muted state" role="status">{hint}</p>{/if}
  <div class="bar">
    {#if canDictate(settings.serverStt)}
      <button class="orb" class:live={status === 'listening'} aria-label={status === 'listening' ? t('mic.stop') : t('mic.start')} aria-pressed={status === 'listening'} disabled={status === 'processing'} onclick={toggleMic}>
        <Icon name="mic" size={22} />
      </button>
    {/if}
    <textarea class="field" rows="1" placeholder={t('talk.placeholder')} bind:value={text} use:autoresize={text} {onkeydown}></textarea>
    {#if busy}
      <button class="btn btn-primary send" onclick={onstop} aria-label={t('talk.stop')}><Icon name="stop" size={18} /></button>
    {:else}
      <button class="btn btn-primary send" onclick={submit} disabled={!text.trim()} aria-label={t('talk.send')}><Icon name="send" size={18} /></button>
    {/if}
  </div>
  {#if canDictate(settings.serverStt)}
    <button class="link-btn lang" onclick={onlang}>{langLabel}</button>
  {/if}
</div>

<style>
  .composer { display: grid; gap: 0.4rem; }
  .state { text-align: center; font-size: 0.9rem; }
  .bar { display: flex; align-items: flex-end; gap: 0.6rem; }
  textarea { resize: none; border-radius: 22px; max-height: 12rem; }
  .send { width: 3rem; height: 3rem; padding: 0; display: grid; place-items: center; flex: none; }
  .orb { width: 3rem; height: 3rem; flex: none; border-radius: 50%; border: 0; cursor: pointer; display: grid; place-items: center; background: var(--hl); color: var(--hl-ink); }
  .orb:disabled { opacity: 0.5; }
  .orb.live { background: var(--bad); color: #fff; animation: pulse 1.4s ease-out infinite; }
  .lang { justify-self: center; }
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--bad) 55%, transparent); }
    100% { box-shadow: 0 0 0 16px transparent; }
  }
</style>
