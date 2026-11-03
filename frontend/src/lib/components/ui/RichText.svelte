<script lang="ts">
  import { parseRichText } from '$lib/utils/richtext';

  let { text }: { text: string } = $props();
  const blocks = $derived(parseRichText(text));
</script>

<div class="rich">
  {#each blocks as block}
    {#if block.type === 'ul'}
      <ul>
        {#each block.items as item}
          <li>{#each item as seg}{#if seg.bold}<strong>{seg.text}</strong>{:else}{seg.text}{/if}{/each}</li>
        {/each}
      </ul>
    {:else}
      <p>{#each block.segments as seg}{#if seg.bold}<strong>{seg.text}</strong>{:else}{seg.text}{/if}{/each}</p>
    {/if}
  {/each}
</div>

<style>
  .rich { display: grid; gap: 0.7rem; }
  ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 0.3rem; }
</style>
