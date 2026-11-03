<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';

  let { code, model = '', onretry }: { code: string; model?: string; onretry?: () => void } = $props();

  const known = ['backend_unreachable', 'network', 'llm_unavailable', 'model_missing', 'llm_bad_output', 'speech_unavailable', 'audio_too_large', 'not_found'];
  const key = $derived(known.includes(code) ? code : 'unknown');
  const setup = $derived(['backend_unreachable', 'llm_unavailable', 'model_missing'].includes(key));
</script>

<div class="notice" class:notice-warn={setup} class:notice-bad={!setup} role={setup ? 'status' : 'alert'}>
  <strong>{t(`err.${key}.title`)}</strong>
  <p>{t(`err.${key}.hint`, { model })}</p>
  {#if onretry}<button class="link-btn" style="justify-self: start" onclick={onretry}>{t('common.retry')}</button>{/if}
</div>
