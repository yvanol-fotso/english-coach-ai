<script lang="ts">
  import { invalidate } from '$app/navigation';
  import ConversationList from '$lib/components/history/ConversationList.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, deleteConversation } from '$lib/services/api';
  import { pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
  let errorCode = $state('');

  async function remove(id: number) {
    try {
      await deleteConversation(id);
      await invalidate('app:history');
    } catch (e) {
      errorCode = codeOf(e);
    }
  }
</script>

<svelte:head><title>{t('nav.history')} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t('history.title')}</h1>
    <p class="lead">{t('history.lead')}</p>
  </div>

  {#if errorCode}<ErrorNotice code={errorCode} />{/if}

  {#if data.conversations === null}
    <ErrorNotice code="backend_unreachable" />
  {:else if data.conversations.length === 0}
    <p class="muted">{t('history.empty')}</p>
  {:else}
    <ConversationList
      items={data.conversations}
      labelOf={(id) => { const found = data.catalog?.scenarios.find((s) => s.id === id); return found ? pick(found.label) : id; }}
      ondelete={remove}
    />
  {/if}
</section>
