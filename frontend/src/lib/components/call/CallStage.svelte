<script lang="ts">
  import CorrectionNote from '$lib/components/chat/CorrectionNote.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import Logo from '$lib/components/ui/Logo.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import type { VoicePhase } from '$lib/services/voiceLoop.svelte';
  import type { ChatMessage } from '$lib/types';

  let {
    title,
    time,
    phase,
    active,
    heard,
    captions,
    showCaptions,
    muted,
    micLabel,
    onmute,
    oncaptions,
    onlang,
    onskip,
    onresume,
    onhangup
  }: {
    title: string;
    time: string;
    phase: VoicePhase;
    active: boolean;
    heard: string;
    captions: ChatMessage[];
    showCaptions: boolean;
    muted: boolean;
    micLabel: string;
    onmute: () => void;
    oncaptions: () => void;
    onlang: () => void;
    onskip: () => void;
    onresume: () => void;
    onhangup: () => void;
  } = $props();

  const coach = $derived([...captions].reverse().find((m) => m.role === 'assistant'));
  const learner = $derived([...captions].reverse().find((m) => m.role === 'user'));
  const status = $derived(!active ? t('live.nospeech') : phase === 'muted' ? t('call.muted') : t(`live.${phase}`));
</script>

<div class="call">
  <div class="top"><span>{title}</span><span class="time">{time}</span></div>

  <div class="center">
    <div class="avatar {active ? phase : 'idle'}"><Logo size={104} /></div>
    <p class="status" role="status">{status}</p>
    {#if active && phase === 'listening' && heard}<p class="heard muted">{heard}</p>{/if}
  </div>

  {#if showCaptions}
    <div class="captions" aria-live="polite">
      {#if coach}<p class="coach">{coach.content}</p>{/if}
      {#if learner}
        <p class="me muted">{learner.content}</p>
        {#if learner.correction}<CorrectionNote correction={learner.correction} original={learner.content} />{/if}
      {/if}
    </div>
  {/if}

  <div class="controls">
    <button class="round" aria-pressed={muted} aria-label={muted ? t('call.unmute') : t('call.mute')} onclick={onmute} disabled={!active}>
      <Icon name={muted ? 'micoff' : 'mic'} size={22} />
    </button>
    <button class="round" aria-pressed={showCaptions} aria-label={t('call.captions')} onclick={oncaptions}><Icon name="chat" size={22} /></button>
    {#if active && phase === 'speaking'}
      <button class="round" aria-label={t('live.skip')} onclick={onskip}><Icon name="stop" size={20} /></button>
    {:else if !active}
      <button class="round" aria-label={t('common.retry')} onclick={onresume}><Icon name="mic" size={22} /></button>
    {/if}
    <button class="round hang" aria-label={t('call.end')} onclick={onhangup}><Icon name="phone" size={24} /></button>
  </div>
  <button class="link-btn lang" onclick={onlang}>{micLabel}</button>
</div>

<style>
  .call { flex: 1; display: grid; grid-template-rows: auto 1fr auto auto auto; gap: 1.2rem; justify-items: center; padding: 0.5rem 0 1rem; }
  .top { display: flex; gap: 1rem; font-weight: 600; color: var(--muted); }
  .time { font-variant-numeric: tabular-nums; }
  .center { display: grid; align-content: center; justify-items: center; gap: 0.8rem; }
  .avatar { border-radius: 50%; padding: 0.7rem; background: var(--accent-soft); }
  .avatar.listening { animation: ring 1.6s ease-out infinite; }
  .avatar.speaking { animation: ring 1.1s ease-out infinite; background: var(--hl-soft); }
  .avatar.thinking { opacity: 0.8; }
  .status { font: 650 1.25rem var(--font-display); }
  .heard { max-width: 28rem; text-align: center; }
  .captions { width: min(36rem, 100%); display: grid; gap: 0.6rem; text-align: center; }
  .coach { font-size: 1.15rem; }
  .me { font-size: 0.95rem; }
  .controls { display: flex; gap: 1rem; }
  .round { width: 3.6rem; height: 3.6rem; border-radius: 50%; border: 1px solid var(--line); background: var(--surface); color: var(--ink); display: grid; place-items: center; cursor: pointer; }
  .round[aria-pressed='true'] { background: var(--accent-soft); border-color: var(--accent); color: var(--accent); }
  .round:disabled { opacity: 0.4; }
  .hang { background: var(--bad); border-color: var(--bad); color: #fff; }
  .hang :global(svg) { transform: rotate(135deg); }
  @keyframes ring {
    0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--accent) 40%, transparent); }
    100% { box-shadow: 0 0 0 28px transparent; }
  }
</style>
