<script lang="ts">
  import { invalidateAll } from '$app/navigation';
  import { t } from '$lib/i18n/index.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import type { CatalogLanguage } from '$lib/types';

  let { languages }: { languages: CatalogLanguage[] } = $props();

  async function choose(event: Event) {
    preferences.setTarget((event.currentTarget as HTMLSelectElement).value);
    await invalidateAll();
  }
</script>

<label class="target">
  <span class="muted">{t('target.label')}</span>
  <select class="field" value={preferences.target} onchange={choose}>
    {#each languages.filter((l) => l.available) as language}<option value={language.code}>{language.native}</option>{/each}
  </select>
</label>

<style>
  .target { display: grid; gap: 0.25rem; padding-inline: 0.5rem; font-size: 0.8rem; }
  select { padding: 0.4rem 0.6rem; font-size: 0.92rem; }
  @media (max-width: 760px) { .target { display: none; } }
</style>
