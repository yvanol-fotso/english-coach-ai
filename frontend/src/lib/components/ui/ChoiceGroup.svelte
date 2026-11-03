<script lang="ts" generics="T extends string">
  let {
    label,
    options,
    value,
    onchange
  }: { label: string; options: { value: T; label: string }[]; value: T; onchange: (value: T) => void } = $props();
</script>

<div class="stack">
  <span class="muted">{label}</span>
  <div class="row" role="group" aria-label={label}>
    {#each options as option}
      <button class="chip" aria-pressed={value === option.value} onclick={() => onchange(option.value)}>{option.label}</button>
    {/each}
  </div>
</div>
