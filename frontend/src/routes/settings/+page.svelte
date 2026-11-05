<script lang="ts">
  import { onMount } from 'svelte';
  import { invalidateAll } from '$app/navigation';
  import ChoiceGroup from '$lib/components/ui/ChoiceGroup.svelte';
  import LanguagePicker from '$lib/components/ui/LanguagePicker.svelte';
  import LevelCards from '$lib/components/ui/LevelCards.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import { settings } from '$lib/stores/settings.svelte';
  import { FALLBACK_LANGUAGES } from '$lib/data/languages';
  import type { Accent, Lang, Theme } from '$lib/types';
  import { listVoices } from '$lib/services/speech';
  import { setCookie } from '$lib/utils/cookies';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
  let name = $state('');
  $effect.pre(() => {
    name = data.profile ?? '';
  });

  async function saveProfile(event: SubmitEvent) {
    event.preventDefault();
    setCookie('ec_profile', name.trim());
    await invalidateAll();
  }

  let voices = $state<SpeechSynthesisVoice[]>([]);
  onMount(() => {
    if (!('speechSynthesis' in window)) return;
    const refresh = () => (voices = listVoices('en'));
    refresh();
    speechSynthesis.addEventListener('voiceschanged', refresh);
    return () => speechSynthesis.removeEventListener('voiceschanged', refresh);
  });

  const themes: Theme[] = ['system', 'light', 'dark'];
  const accents: Accent[] = ['teal', 'blue', 'plum', 'ember'];
</script>

<svelte:head><title>{t('nav.settings')} · English Coach</title></svelte:head>

<section class="page">
  <h1>{t('settings.title')}</h1>

  <form class="card stack" onsubmit={saveProfile}>
    <h2>{t('settings.profile')}</h2>
    <p class="muted">{t('settings.profile.hint')}</p>
    <div class="row">
      <input class="field name" bind:value={name} maxlength="40" aria-label={t('settings.profile.name')} placeholder={t('settings.profile.name')} />
      <button class="btn btn-primary" disabled={!name.trim() || name.trim() === data.profile}>{t('settings.profile.save')}</button>
    </div>
  </form>

  <div class="card stack">
    <h2>{t('settings.target')}</h2>
    <LanguagePicker languages={data.catalog?.languages ?? FALLBACK_LANGUAGES} />
  </div>

  <div class="card stack">
    <h2>{t('settings.language')}</h2>
    <ChoiceGroup
      label={t('settings.language')}
      value={preferences.lang}
      options={[{ value: 'fr', label: 'Français' }, { value: 'en', label: 'English' }]}
      onchange={(lang) => preferences.setLang(lang)}
    />
  </div>

  <div class="card stack">
    <h2>{t('settings.appearance')}</h2>
    <ChoiceGroup
      label={t('settings.theme')}
      value={preferences.theme}
      options={themes.map((value) => ({ value, label: t(`theme.${value}`) }))}
      onchange={(theme) => preferences.setTheme(theme)}
    />
    <ChoiceGroup
      label={t('settings.accent')}
      value={preferences.accent}
      options={accents.map((value) => ({ value, label: t(`accent.${value}`) }))}
      onchange={(accent) => preferences.setAccent(accent)}
    />
  </div>

  <div class="card stack">
    <h2>{t('settings.level')}</h2>
    <LevelCards />
  </div>

  <div class="card stack">
    <h2>{t('settings.voice')}</h2>
    <label class="stack">
      <span class="muted">{t('settings.voice.speed')} : {settings.speechRate.toFixed(2)}×</span>
      <input type="range" min="0.6" max="1.2" step="0.05" bind:value={settings.speechRate} />
    </label>
    <label class="toggle"><input type="checkbox" bind:checked={settings.autoSpeak} /> {t('settings.voice.autospeak')}</label>
    {#if voices.length}
      <label class="stack">
        <span class="muted">{t('settings.voice.name')}</span>
        <select class="field" bind:value={settings.voiceName}>
          <option value="">{t('settings.voice.default')}</option>
          {#each voices as voice}<option value={voice.name}>{voice.name}</option>{/each}
        </select>
      </label>
    {/if}
    <p>
      <strong>{t('settings.voice.server')} :</strong>
      {data.health.stt && data.health.tts ? t('settings.voice.on') : t('settings.voice.off')}
      <span class="muted"> · {t('settings.voice.browser')}</span>
    </p>
  </div>
</section>

<style>
  .toggle { display: flex; align-items: center; gap: 0.6rem; cursor: pointer; }
  .name { flex: 1; min-width: 10rem; width: auto; }
  input[type='range'] { accent-color: var(--accent); width: 100%; }
</style>
