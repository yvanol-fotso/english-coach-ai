<script lang="ts">
  const paths = {
    home: '<path d="M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    chat: '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-5.4A8 8 0 1 1 21 12z"/>',
    mic: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    translate: '<path d="M4 7h13l-3-3M20 17H7l3 3"/>',
    pencil: '<path d="M4 20l1-4L16 5l3 3L8 19z"/>',
    book: '<path d="M6 3h13v15H6a2 2 0 0 0-2 2V5a2 2 0 0 1 2-2zM6 18v3h13"/>',
    bookmark: '<path d="M6 3h12v18l-6-4-6 4z"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    sliders: '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    send: '<path d="M4 12l16-8-6 16-2-7z"/>',
    stop: '<rect x="6" y="6" width="12" height="12" rx="2"/>',
    feather: '<path d="M20 4c-8 0-14 5-14 13v3h3c8 0 11-6 11-16zM6 20L16 10"/>',
    wave: '<path d="M3 12h2M8 7v10M13 4v16M18 8v8M21 12h0"/>',
    grid: '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    check: '<path d="M5 12l5 5L20 7"/>',
    phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    question: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h0"/>',
    route: '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a3 3 0 0 0 0-6h-4a3 3 0 0 1 0-6h6"/>',
    micoff: '<path d="M3 3l18 18M9 5a3 3 0 0 1 6 0v5M15 14a3 3 0 0 1-5.5 1.5M5 11a7 7 0 0 0 11 5.5M12 18v3"/>',
    trash: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>'
  };

  let { name, size = 20 }: { name: keyof typeof paths; size?: number } = $props();
</script>

<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  {@html paths[name]}
</svg>
