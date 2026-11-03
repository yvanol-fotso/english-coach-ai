<script lang="ts">
  import ChoiceGroup from '$lib/components/ui/ChoiceGroup.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import RichText from '$lib/components/ui/RichText.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, isAbort, streamTool } from '$lib/services/api';
  import { canSpeak, speak, speakable, stopSpeaking } from '$lib/services/speech';
  import { settings } from '$lib/stores/settings.svelte';
  import { pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  const tool = $derived(data.catalog?.tools.find((entry) => entry.id === data.id));
  let input = $state('');
  let chosen = $state<Record<string, string>>({});
  let output = $state('');
  let loading = $state(false);
  let errorCode = $state('');
  let copied = $state(false);
  let controller: AbortController | null = null;

  const options = $derived(Object.fromEntries((tool?.options ?? []).map((o) => [o.id, chosen[o.id] ?? o.choices[0].id])));

  async function run() {
    if (!tool) return;
    controller?.abort();
    controller = new AbortController();
    output = '';
    errorCode = '';
    loading = true;
    try {
      for await (const token of streamTool(tool.id, { input: input.trim(), options, level: settings.level }, controller.signal)) output += token;
    } catch (e) {
      if (!isAbort(e)) errorCode = codeOf(e);
    } finally {
      loading = false;
    }
  }

  async function copy() {
    await navigator.clipboard.writeText(output);
    copied = true;
    setTimeout(() => (copied = false), 1500);
  }
</script>

<svelte:head><title>{tool ? pick(tool.title) : t('nav.studio')} · English Coach</title></svelte:head>

<section class="page">
  <a class="link-btn back" href="/studio">← {t('studio.back')}</a>

  {#if tool}
    <div class="page-head">
      <h1>{pick(tool.title)}</h1>
      <p class="lead">{pick(tool.description)}</p>
    </div>

    <textarea class="field" rows="5" bind:value={input} placeholder={pick(tool.placeholder)}></textarea>

    {#each tool.options as option}
      <ChoiceGroup
        label={pick(option.label)}
        value={options[option.id]}
        options={option.choices.map((c) => ({ value: c.id, label: pick(c.label) }))}
        onchange={(value) => (chosen[option.id] = value)}
      />
    {/each}

    <div class="row">
      <button class="btn btn-primary" onclick={run} disabled={loading || !input.trim()}>
        {loading ? t('studio.generating') : output ? t('studio.again') : t('studio.generate')}
      </button>
      <LevelSelect />
    </div>

    {#if errorCode}<ErrorNotice code={errorCode} onretry={run} />{/if}

    {#if output}
      <article class="card stack">
        <RichText text={output} />
        {#if !loading}
          <div class="row">
            <button class="btn btn-sm" onclick={copy}>{copied ? t('common.copied') : t('common.copy')}</button>
            {#if canSpeak()}
              <button class="btn btn-sm" onclick={() => speak(speakable(output), { rate: settings.speechRate, server: settings.serverTts, voice: settings.voiceName })}>{t('common.listen')}</button>
              <button class="btn btn-sm" onclick={stopSpeaking}>{t('common.stop')}</button>
            {/if}
          </div>
        {/if}
      </article>
    {/if}
  {:else}
    <ErrorNotice code="backend_unreachable" />
  {/if}
</section>

<style>
  .back { justify-self: start; }
</style>
