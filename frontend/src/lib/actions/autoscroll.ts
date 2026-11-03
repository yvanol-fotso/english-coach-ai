import type { Action } from 'svelte/action';

export const autoscroll: Action<HTMLElement> = (node) => {
  const toBottom = () => node.scrollTo({ top: node.scrollHeight });
  const observer = new MutationObserver(toBottom);
  observer.observe(node, { childList: true, subtree: true, characterData: true });
  toBottom();
  return { destroy: () => observer.disconnect() };
};
