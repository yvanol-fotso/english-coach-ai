<script lang="ts">
  import { untrack } from 'svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import ReviewCard from '$lib/components/vocabulary/ReviewCard.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, logActivity, reviewWord } from '$lib/services/api';
  import type { ReviewGrade } from '$lib/types';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  const queue = untrack(() => data.queue ?? []);
  const total = queue.length;
  let position = $state(0);
  let good = $state(0);
  let errorCode = $state('');

  async function grade(value: ReviewGrade) {
    try {
      await reviewWord(queue[position].id, value);
    } catch (e) {
      errorCode = codeOf(e);
      return;
    }
    if (value === 'good' || value === 'easy') good++;
    position++;
    if (position >= total) {
      logActivity('vocabulary', Math.round((good / total) * 100), { title: 'review', count: total }).catch(() => {});
    }
  }
</script>

<svelte:head><title>{t('review.title')} · English Coach</title></svelte:head>

<section class="page">
  <a class="link-btn back" href="/vocabulary">← {t('review.back')}</a>
  <h1>{t('review.title')}</h1>

  {#if data.queue === null}
    <ErrorNotice code="backend_unreachable" />
  {:else if total === 0}
    <p class="muted">{t('review.none')}</p>
  {:else if position >= total}
    <p class="lead">{t('review.done')}</p>
  {:else}
    <p class="muted">{t('review.progress', { i: position + 1, n: total })}</p>
    {#key queue[position].id}<ReviewCard word={queue[position]} ongrade={grade} />{/key}
  {/if}
  {#if errorCode}<ErrorNotice code={errorCode} />{/if}
</section>

<style>
  .back { justify-self: start; }
</style>
