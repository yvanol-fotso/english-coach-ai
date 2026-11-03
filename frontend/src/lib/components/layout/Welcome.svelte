<script lang="ts">
  import { invalidateAll } from '$app/navigation';
  import ChoiceGroup from '$lib/components/ui/ChoiceGroup.svelte';
  import LevelCards from '$lib/components/ui/LevelCards.svelte';
  import { t } from '$lib/i18n/index.svelte';
  import { preferences } from '$lib/stores/preferences.svelte';
  import type { Lang } from '$lib/types';
  import { setCookie } from '$lib/utils/cookies';

  let name = $state('');

  async function start(event: SubmitEvent) {
    event.preventDefault();
    setCookie('ec_profile', name.trim());
    await invalidateAll();
  }
</script>

<div class="backdrop" role="dialog" aria-modal="true" aria-labelledby="welcome-title" tabindex="-1">
  <form class="card dialog stack" onsubmit={start}>
    <div class="stack">
      <h1 id="welcome-title">{t('welcome.title')}</h1>
      <p class="lead">{t('welcome.lead')}</p>
    </div>
    <ChoiceGroup
      label={t('welcome.language')}
      value={preferences.lang}
      options={[{ value: 'fr', label: 'Français' }, { value: 'en', label: 'English' }]}
      onchange={(lang) => preferences.setLang(lang)}
    />
    <label class="stack">
      <span class="muted">{t('welcome.name')}</span>
      <input class="field" bind:value={name} maxlength="40" required />
    </label>
    <div class="stack">
      <span class="muted">{t('welcome.level')}</span>
      <LevelCards />
    </div>
    <button class="btn btn-primary" disabled={!name.trim()}>{t('welcome.start')}</button>
  </form>
</div>

<style>
  .backdrop { position: fixed; inset: 0; z-index: 10; background: rgb(10 14 20 / 0.55); display: grid; place-items: center; padding: 1rem; overflow-y: auto; }
  .dialog { width: min(34rem, 100%); max-height: 100%; overflow-y: auto; gap: 1.25rem; }
</style>
