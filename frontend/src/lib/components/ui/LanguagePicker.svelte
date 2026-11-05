<script lang="ts">
  import { invalidateAll } from '$app/navigation';
  import { t } from '$lib/i18n/index.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import type { CatalogLanguage } from '$lib/types';
  import { pick } from '$lib/utils/format';

  let { languages }: { languages: CatalogLanguage[] } = $props();

  async function choose(code: string) {
    preferences.setTarget(code);
    await invalidateAll();
  }
</script>

<div class="row" role="group" aria-label={t('target.label')}>
  {#each languages as language}
    <button class="chip" aria-pressed={preferences.target === language.code} disabled={!language.available} onclick={() => choose(language.code)}>
      {language.native}{#if !language.available}<span class="soon">{t('target.soon')}</span>{/if}
    </button>
  {/each}
</div>

<style>
  .chip:disabled { opacity: 0.55; cursor: not-allowed; border-style: dashed; }
  .soon { margin-left: 0.4rem; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
</style>
