<script lang="ts">
  import '../app.css';
  import type { Snippet } from 'svelte';
  import { onMount } from 'svelte';
  import Sidebar from '$lib/components/layout/Sidebar.svelte';
  import Welcome from '$lib/components/layout/Welcome.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { settings } from '$lib/stores/settings.svelte';
  import { FALLBACK_LANGUAGES } from '$lib/data/languages';
  import { setCookie } from '$lib/utils/cookies';
  import type { LayoutData } from './$types';

  let { data, children }: { data: LayoutData; children: Snippet } = $props();

  const initPreferences = () => preferences.init(data.prefs);
  initPreferences();

  onMount(() => {
    settings.load();
    setCookie('ec_tz', String(-new Date().getTimezoneOffset()));
  });

  $effect(() => settings.persist());
  $effect(() => {
    settings.serverStt = data.health.stt;
    settings.serverTts = data.health.tts;
  });
  $effect(() => {
    if (preferences.theme !== 'system') return;
    const query = matchMedia('(prefers-color-scheme: dark)');
    const sync = () => preferences.apply();
    query.addEventListener('change', sync);
    return () => query.removeEventListener('change', sync);
  });
</script>

<div class="shell">
  <Sidebar health={data.health} profile={data.profile} languages={data.catalog?.languages ?? FALLBACK_LANGUAGES} />
  <main>{@render children()}</main>
</div>

{#if data.profile === null}<Welcome languages={data.catalog?.languages ?? FALLBACK_LANGUAGES} />{/if}

<style>
  .shell { display: grid; grid-template-columns: 16rem 1fr; min-height: 100dvh; }
  main { min-width: 0; height: 100dvh; overflow-y: auto; }
  @media (max-width: 760px) {
    .shell { grid-template-columns: 1fr; grid-template-rows: 1fr auto; height: 100dvh; }
    main { height: auto; min-height: 0; }
  }
</style>
