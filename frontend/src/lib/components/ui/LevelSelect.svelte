<script lang="ts">
  import { levels } from '$lib/data/topics';
  import { t } from '$lib/i18n/index.svelte';
  import { settings } from '$lib/stores/settings.svelte';
</script>

<label class="select">
  <span class="sr-only">{t('common.level')}</span>
  <select class="field" bind:value={settings.level}>
    {#each levels as level}<option value={level}>{level} · {t(`level.${level}.name`)}</option>{/each}
  </select>
</label>

<style>
  select { padding: 0.35rem 0.7rem; border-radius: 999px; font-size: 0.9rem; width: auto; }
</style>
