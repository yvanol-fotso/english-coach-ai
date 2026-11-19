<script lang="ts">
  import { parseRichText, type Leaf, type Segment } from '$lib/utils/richtext';

  let { text }: { text: string } = $props();
  const blocks = $derived(parseRichText(text));
</script>

{#snippet inline(segments: Segment[])}
  {#each segments as seg}{#if seg.bold}<strong>{seg.text}</strong>{:else if seg.italic}<em>{seg.text}</em>{:else}{seg.text}{/if}{/each}
{/snippet}

{#snippet leaf(block: Leaf)}
  {#if block.type === 'h'}
    <h3>{@render inline(block.segments)}</h3>
  {:else if block.type === 'p'}
    <p>{#each block.lines as line, i}{#if i}<br />{/if}{@render inline(line)}{/each}</p>
  {:else if block.type === 'ul'}
    <ul>{#each block.items as item}<li>{@render inline(item)}</li>{/each}</ul>
  {:else}
    <ol>{#each block.items as item}<li>{@render inline(item)}</li>{/each}</ol>
  {/if}
{/snippet}

<div class="rich">
  {#each blocks as block}
    {#if block.type === 'answers'}
      <details>
        <summary>{@render inline(block.title)}</summary>
        <div class="inner">{#each block.blocks as inner}{@render leaf(inner)}{/each}</div>
      </details>
    {:else}
      {@render leaf(block)}
    {/if}
  {/each}
</div>

<style>
  .rich { display: grid; gap: 0.8rem; }
  h3 { margin: 0.6rem 0 0; font: 650 0.8rem var(--font-display); text-transform: uppercase; letter-spacing: 0.06em; color: var(--accent); }
  h3:first-child { margin-top: 0; }
  p { margin: 0; line-height: 1.6; }
  ul, ol { margin: 0; padding-left: 1.3rem; display: grid; gap: 0.4rem; line-height: 1.5; }
  details { border: 1px solid color-mix(in srgb, currentColor 18%, transparent); border-radius: 12px; padding: 0.6rem 0.9rem; }
  summary { cursor: pointer; font-weight: 650; color: var(--accent); }
  .inner { display: grid; gap: 0.6rem; margin-top: 0.6rem; }
</style>