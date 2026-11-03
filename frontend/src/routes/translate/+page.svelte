<script lang="ts">
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import TranslationCard from '$lib/components/translate/TranslationCard.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, translate } from '$lib/services/api';
  import type { Language, TranslationResult } from '$lib/types';

  let text = $state('');
  let source = $state<Language | 'auto'>('auto');
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
      <button aria-pressed={source === 'fr'} onclick={() => (source = 'fr')}>FR</button>
      <button aria-pressed={source === 'en'} onclick={() => (source = 'en')}>EN</button>
    </div>
    <button class="btn btn-primary" onclick={run} disabled={loading || !text.trim()}>
      {loading ? t('translate.loading') : t('translate.submit')}
    </button>
  </div>
  {#if errorCode}<ErrorNotice code={errorCode} onretry={run} />{/if}
  {#if result}<TranslationCard {result} />{/if}
</section>
