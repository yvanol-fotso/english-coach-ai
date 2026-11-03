<script lang="ts">
  import CorrectionCard from '$lib/components/correct/CorrectionCard.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, correct } from '$lib/services/api';
  import { settings } from '$lib/stores/settings.svelte';
  import type { CorrectionResult } from '$lib/types';

  let text = $state('');
  let result = $state<CorrectionResult | null>(null);
  let loading = $state(false);
  let errorCode = $state('');

  async function run() {
    loading = true;
    errorCode = '';
    try {
      result = await correct(text.trim(), settings.level);
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head><title>{t('nav.write')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('write.title')}</h1>
    <p class="lead">{t('write.lead')}</p>
  </div>
  <textarea class="field" rows="7" bind:value={text} placeholder={t('write.placeholder')}></textarea>
  <div class="row">
    <button class="btn btn-primary" onclick={run} disabled={loading || !text.trim()}>
      {loading ? t('write.loading') : t('write.submit')}
    </button>
    <LevelSelect />
  </div>
  {#if errorCode}<ErrorNotice code={errorCode} onretry={run} />{/if}
  {#if result}<CorrectionCard {result} />{/if}
</section>
