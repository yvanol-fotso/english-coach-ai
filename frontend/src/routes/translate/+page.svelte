<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import TranslationCard from '$lib/components/translate/TranslationCard.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { langName } from '$lib/utils/format';
  import { codeOf, translate } from '$lib/services/api';
  import type { TranslationResult } from '$lib/types';

  let text = $state('');
  let source = $state<'auto' | 'native' | 'target'>('auto');
  const nativeCode = $derived(preferences.lang !== preferences.target ? preferences.lang : preferences.target === 'fr' ? 'en' : 'fr');
  let result = $state<TranslationResult | null>(null);
  let loading = $state(false);
  let errorCode = $state('');

  async function run() {
    loading = true;
    errorCode = '';
    try {
      result = await translate(text.trim(), source);
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head><title>{t('nav.translate')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('translate.title')}</h1>
    <p class="lead">{t('translate.lead')}</p>
  </div>
  <textarea class="field" rows="5" bind:value={text} placeholder={t('translate.placeholder')}></textarea>
  <div class="row">
    <div class="seg" role="group" aria-label="Source">
      <button aria-pressed={source === 'auto'} onclick={() => (source = 'auto')}>{t('translate.auto')}</button>
      <button aria-pressed={source === 'native'} onclick={() => (source = 'native')}>{langName(nativeCode)}</button>
      <button aria-pressed={source === 'target'} onclick={() => (source = 'target')}>{langName(preferences.target)}</button>
    </div>
    <button class="btn btn-primary" onclick={run} disabled={loading || !text.trim()}>
      {loading ? t('translate.loading') : t('translate.submit')}
    </button>
  </div>
  {#if errorCode}<ErrorNotice code={errorCode} onretry={run} />{/if}
  {#if result}<TranslationCard {result} />{/if}
</section>
