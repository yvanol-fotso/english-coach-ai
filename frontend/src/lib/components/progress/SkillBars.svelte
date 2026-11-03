<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import type { Skill } from '$lib/types';

  let { counts }: { counts: Record<Skill, number> } = $props();

  const skills = $derived(Object.keys(counts) as Skill[]);
  const max = $derived(Math.max(1, ...Object.values(counts)));
</script>

<div class="bars">
  {#each skills as skill}
    <div class="line">
      <span>{t(`skill.${skill}`)}</span>
      <div class="track"><div class="fill" style="width: {(counts[skill] / max) * 100}%"></div></div>
      <strong>{counts[skill]}</strong>
    </div>
  {/each}
</div>

<style>
  .bars { display: grid; gap: 0.7rem; }
  .line { display: grid; grid-template-columns: 11rem 1fr 2.5rem; align-items: center; gap: 0.8rem; }
  .track { height: 0.7rem; background: var(--surface-2); border-radius: 999px; overflow: hidden; }
  .fill { height: 100%; background: var(--accent); border-radius: 999px; }
  strong { text-align: right; }
  @media (max-width: 520px) { .line { grid-template-columns: 8rem 1fr 2rem; } }
</style>
