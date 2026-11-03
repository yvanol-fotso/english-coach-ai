<script lang="ts">
  import { page } from '$app/state';
  import { t } from '$lib/i18n/index.svelte';

  const key = $derived(page.status === 404 ? '404' : '500');
</script>

<svelte:head><title>{page.status} · English Coach</title></svelte:head>

<section class="page">
  <div class="page-head">
    <h1>{t(`err.page.${key}.title`)}</h1>
    <p class="lead">{t(`err.page.${key}.hint`)}</p>
  </div>
  <a class="btn btn-primary" href="/" style="justify-self: start; text-decoration: none">{t('common.back')}</a>
</section>
