<script lang="ts">
  import { autoscroll } from '$lib/actions/autoscroll';
  import type { ChatMessage } from '$lib/types';
  import ChatBubble from './ChatBubble.svelte';

  let { messages, busy }: { messages: ChatMessage[]; busy: boolean } = $props();
</script>

<div class="thread" use:autoscroll aria-live="polite">
  {#each messages as message, i}
    <ChatBubble {message} streaming={busy && i === messages.length - 1} />
  {/each}
</div>

<style>
  .thread { display: flex; flex-direction: column; gap: 1rem; overflow-y: auto; flex: 1; padding: 0.5rem 0.25rem 1rem; }
</style>
