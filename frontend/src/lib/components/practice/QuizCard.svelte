<script lang="ts">
  import { t } from '$lib/i18n/index.svelte';
  import type { Question } from '$lib/types';

  let { questions, onchecked }: { questions: Question[]; onchecked?: (score: number, total: number) => void } = $props();

  let answers = $state<number[]>([]);
  let checked = $state(false);

  const score = $derived(questions.filter((q, i) => answers[i] === q.answer_index).length);

  function check() {
    checked = true;
    onchecked?.(score, questions.length);
  }
</script>

<div class="stack">
  {#each questions as q, i}
    <fieldset class="card stack">
      <legend>{i + 1}. {q.question}</legend>
      {#each q.choices as choice, c}
        <label class:right={checked && c === q.answer_index} class:wrong={checked && answers[i] === c && c !== q.answer_index}>
          <input type="radio" name="q{i}" value={c} bind:group={answers[i]} disabled={checked} />
          {choice}
        </label>
      {/each}
      {#if checked}<p class="muted">{q.explanation}</p>{/if}
    </fieldset>
  {/each}

  {#if checked}
    <p><strong>{t('quiz.score', { score, total: questions.length })}</strong></p>
  {:else}
    <button class="btn btn-primary" style="justify-self: start" onclick={check}>{t('quiz.check')}</button>
  {/if}
</div>

<style>
  fieldset { margin: 0; }
  legend { font-weight: 600; padding: 0; }
  label { display: flex; gap: 0.6rem; align-items: center; padding: 0.4rem 0.6rem; border-radius: 8px; border: 1px solid transparent; }
  .right { border-color: var(--ok); }
  .wrong { border-color: var(--bad); }
</style>
