<script lang="ts">
  import { invalidate } from '$app/navigation';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import ExplanationCard from '$lib/components/vocabulary/ExplanationCard.svelte';
  import WordList from '$lib/components/vocabulary/WordList.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, explain, removeWord, saveWord } from '$lib/services/api';
  import { settings } from '$lib/stores/settings.svelte';
  import type { Explanation } from '$lib/types';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  let term = $state('');
  let result = $state<Explanation | null>(null);
  let loading = $state(false);
  let errorCode = $state('');

  const words = $derived(data.words ?? []);
  const saved = $derived(!!result && words.some((w) => w.term.toLowerCase() === result!.term.toLowerCase()));

  async function run(event: SubmitEvent) {
    event.preventDefault();
    if (!term.trim()) return;
    loading = true;
    errorCode = '';
    try {
      result = await explain(term.trim(), settings.level);
    } catch (e) {
      errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }

  async function mutate(action: () => Promise<unknown>) {
    try {
      await action();
      await invalidate('app:words');
    } catch (e) {
      errorCode = codeOf(e);
    }
  }
</script>

<svelte:head><title>{t('nav.vocabulary')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('vocab.title')}</h1>
    <p class="lead">{t('vocab.lead')}</p>
  </div>

  <form class="row" onsubmit={run}>
    <input class="field term" bind:value={term} placeholder={t('vocab.placeholder')} maxlength="200" />
    <button class="btn btn-primary" disabled={loading || !term.trim()}>{loading ? t('vocab.loading') : t('vocab.submit')}</button>
    <LevelSelect />
  </form>

  {#if errorCode}<ErrorNotice code={errorCode} />{/if}
  {#if result}<ExplanationCard word={result} {saved} onsave={() => mutate(() => saveWord(result!))} />{/if}

  {#if words.length}
    <div class="row between">
      <h2>{t('vocab.list', { n: words.length })}</h2>
      {#if data.dueCount > 0}<a class="btn btn-primary btn-sm" href="/vocabulary/review" style="text-decoration: none">{t('vocab.review', { n: data.dueCount })}</a>{/if}
    </div>
    <WordList {words} onremove={(id) => mutate(() => removeWord(id))} />
  {/if}
</section>

<style>
  .between { justify-content: space-between; }
  .term { flex: 1; min-width: 12rem; width: auto; }
</style>
