<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, translate } from '$lib/services/api';
  import { canSpeak, speak, speakable } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import type { ChatMessage, TranslationResult } from '$lib/types';
  import CorrectionNote from './CorrectionNote.svelte';

  let { message, streaming = false }: { message: ChatMessage; streaming?: boolean } = $props();

  const mine = $derived(message.role === 'user');
  let translation = $state<TranslationResult | null>(null);
  let busy = $state(false);
  let errorCode = $state('');

  async function translateToFrench() {
    busy = true;
    errorCode = '';
    try {
      translation = await translate(message.content, 'en');
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      busy = false;
    }
  }
</script>

<div class="turn" class:mine>
  <div class="bubble"><p>{message.content}</p></div>

  {#if mine && message.correction}
    <div class="side"><CorrectionNote correction={message.correction} original={message.content} /></div>
  {/if}

  {#if !mine && message.content && !streaming}
    <div class="actions">
      {#if canSpeak()}
        <button class="link-btn" onclick={() => speak(speakable(message.content), { rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName })}>{t('common.listen')}</button>
      {/if}
      <button class="link-btn" onclick={translateToFrench} disabled={busy}>{t('bubble.translate')}</button>
    </div>
  {/if}

  {#if translation}<p class="note">{translation.translation}</p>{/if}
  {#if errorCode}<div class="side"><ErrorNotice code={errorCode} /></div>{/if}
</div>

<style>
  .turn { display: grid; gap: 0.35rem; justify-items: start; max-width: min(38rem, 92%); }
  .turn.mine { align-self: flex-end; justify-items: end; }
  .bubble { padding: 0.75rem 1rem; border-radius: 18px 18px 18px 6px; background: var(--surface); border: 1px solid var(--line); white-space: pre-wrap; }
  .mine .bubble { border-radius: 18px 18px 6px 18px; background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }
  .actions { display: flex; gap: 1rem; padding-inline: 0.4rem; }
  .note { padding: 0.6rem 0.9rem; border-radius: 12px; background: var(--hl-soft); border: 1px solid var(--hl); }
  .side { width: min(36rem, 100%); }
</style>
