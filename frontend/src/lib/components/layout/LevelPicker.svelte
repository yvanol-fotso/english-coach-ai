<script lang="ts">
  import { settings } from '$lib/stores/settings.svelte';
  import type { Level } from '$lib/types';

  const levels: Level[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
</script>

<label class="picker">
  <span class="muted">Niveau</span>
  <select class="field" bind:value={settings.level}>
    {#each levels as level}<option value={level}>{level}</option>{/each}
  </select>
</label>

<style>
  .picker { display: grid; gap: 0.25rem; font-size: 0.85rem; }
  select { padding: 0.4rem 0.6rem; }
</style>
