<script lang="ts">
  import { levels } from '$lib/data/topics';
  import { t } from '$lib/i18n/index.svelte';
  import { settings } from '$lib/stores/settings.svelte';
</script>

<fieldset class="levels">
  <legend class="sr-only">{t('common.level')}</legend>
  {#each levels as level}
    <label class:on={settings.level === level}>
      <input class="sr-only" type="radio" name="level" value={level} bind:group={settings.level} />
      <span class="code">{level}</span>
      <span class="text">
        <strong>{t(`level.${level}.name`)}</strong>
        <small class="muted">{t(`level.${level}.desc`)}</small>
      </span>
    </label>
  {/each}
</fieldset>

<style>
  .levels { display: grid; gap: 0.5rem; border: 0; padding: 0; margin: 0; }
  label { display: flex; align-items: center; gap: 0.8rem; padding: 0.6rem 0.8rem; border: 1px solid var(--line); border-radius: var(--radius-sm); cursor: pointer; background: var(--surface); }
  label:hover { border-color: var(--accent); }
  label:has(:focus-visible) { outline: 3px solid var(--hl); outline-offset: 2px; }
  label.on { border-color: var(--accent); background: var(--accent-soft); }
  .code { font: 700 0.85rem var(--font-display); min-width: 2rem; text-align: center; padding: 0.15rem 0.4rem; border-radius: 6px; background: var(--surface-2); }
  .on .code { background: var(--accent); color: var(--accent-ink); }
  .text { display: grid; line-height: 1.3; }
</style>
