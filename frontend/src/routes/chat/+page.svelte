<script lang="ts">
  import { untrack } from 'svelte';
  import { goto, invalidate } from '$app/navigation';
  import { page } from '$app/state';
  import ChatComposer from '$lib/components/chat/ChatComposer.svelte';
  import ChatThread from '$lib/components/chat/ChatThread.svelte';
  import ConversationRail from '$lib/components/chat/ConversationRail.svelte';
  import LivePanel from '$lib/components/chat/LivePanel.svelte';
  import TopicPicker from '$lib/components/chat/TopicPicker.svelte';
  import ErrorNotice from '$lib/components/ui/ErrorNotice.svelte';
  import Icon from '$lib/components/ui/Icon.svelte';
  import LevelSelect from '$lib/components/ui/LevelSelect.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { codeOf, getConversation } from '$lib/services/api';
  import { ConversationSession } from '$lib/services/conversation.svelte';
  import { canDictate } from '$lib/services/speech';
  import { VoiceLoop } from '$lib/services/voiceLoop.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { settings } from '$lib/stores/settings.svelte';
  import { langName, pick } from '$lib/utils/format';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();

  const session = new ConversationSession(() => invalidate('app:history'));
  let notice = $state('');
  let micNative = $state(false);
  let openedId: number | null = null;

  const loop = new VoiceLoop({
    lang: () => (micNative ? preferences.nativeLocale : preferences.locale),
    server: () => settings.serverStt,
    turn: (text) => session.send(text),
    speak: () => session.speakLast(true),
    onStall: () => (notice = t('live.nospeech'))
  });

  const situation = $derived(data.catalog?.scenarios.find((s) => s.id === session.scenario && s.chip));
  const micLabel = $derived(t('mic.lang', { lang: langName(micNative ? preferences.lang : preferences.target) }));
  const micLocale = $derived(micNative ? preferences.nativeLocale : preferences.locale);

  function reset() {
    loop.end();
    session.reset();
    notice = '';
  }

  async function open(id: number) {
    reset();
    try {
      const detail = await getConversation(id);
      if (detail.language !== preferences.target) {
        preferences.setTarget(detail.language);
        await invalidate('app:history');
      }
      session.load(detail);
    } catch (e) {
      session.errorCode = codeOf(e);
    }
  }

  $effect(() => {
    const raw = page.url.searchParams.get('c');
    const id = raw ? Number(raw) : null;
    if (id === openedId) return;
    openedId = id;
    untrack(() => (id ? open(id) : reset()));
  });

  async function submit(text: string) {
    const ok = await session.send(text);
    if (ok && settings.autoSpeak) await session.speakLast(false);
  }

  const startNew = () => {
    reset();
    goto('/chat', { replaceState: true });
  };
</script>

<svelte:head><title>{t('nav.talk')} · English Coach</title></svelte:head>

<div class="layout">
  <ConversationRail items={data.conversations ?? []} activeId={session.id} onnew={startNew} />

  <section class="chat">
    <header class="row bar">
      <LevelSelect />
      <label class="toggle">
        <input type="checkbox" checked={settings.feedback === 'inline'} onchange={(e) => (settings.feedback = e.currentTarget.checked ? 'inline' : 'off')} />
        {t('talk.feedback')}
      </label>
      <label class="toggle"><input type="checkbox" bind:checked={settings.autoSpeak} /> {t('talk.autospeak')}</label>
      {#if situation}
        <button class="chip" aria-pressed="true" onclick={() => (session.scenario = 'free')}>{pick(situation.label)} ×</button>
      {/if}
      <span class="spacer"></span>
      {#if canDictate(settings.serverStt)}
        <button class="btn btn-primary" onclick={() => (loop.active ? loop.end() : loop.start())}>
          <Icon name="mic" size={18} /> {loop.active ? t('live.end') : t('live.start')}
        </button>
      {/if}
    </header>

    {#if session.messages.length === 0}
      <TopicPicker catalog={data.catalog} scenario={session.scenario} onstart={submit} onscenario={(id) => (session.scenario = id)} />
    {:else}
      <ChatThread messages={session.messages} busy={session.busy} />
    {/if}

    {#if notice}<p class="notice notice-warn">{notice}</p>{/if}
    {#if session.errorCode}<ErrorNotice code={session.errorCode} />{/if}

    {#if loop.active}
      <LivePanel phase={loop.phase} heard={loop.heard} langLabel={micLabel} onlang={() => (micNative = !micNative)} onskip={() => loop.skip()} onend={() => loop.end()} />
    {:else}
      <ChatComposer busy={session.busy} lang={micLocale} langLabel={micLabel} onlang={() => (micNative = !micNative)} onsend={submit} onstop={() => session.abort()} />
    {/if}
  </section>
</div>

<style>
  .layout { display: flex; height: 100%; }
  .chat { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 1rem; max-width: 52rem; margin-inline: auto; padding: clamp(1rem, 3vw, 2rem); }
  .bar { gap: 0.8rem; }
  .toggle { display: flex; align-items: center; gap: 0.5rem; font-size: 0.88rem; color: var(--muted); cursor: pointer; }
  .spacer { flex: 1; }
</style>
