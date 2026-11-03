<script lang="ts">
  import type { DiffWord } from '$lib/utils/diff';

  let { words }: { words: DiffWord[] } = $props();
</script>

<p class="diff">
  {#each words as w}<span class={w.status}>{w.word}</span>{' '}{/each}
</p>

<style>
  .diff { font-size: 1.15rem; line-height: 1.9; }
  span { padding: 0.1rem 0.3rem; border-radius: 6px; }
  .ok { background: color-mix(in srgb, var(--ok) 20%, transparent); }
  .missing { background: color-mix(in srgb, var(--bad) 22%, transparent); text-decoration: underline; }
  .extra { background: color-mix(in srgb, var(--hl) 40%, transparent); text-decoration: line-through; }
</style>
