import type { Action } from 'svelte/action';

export const autoresize: Action<HTMLTextAreaElement, string> = (node) => {
  const fit = () => {
    node.style.height = 'auto';
    node.style.height = `${Math.min(node.scrollHeight, 200)}px`;
  };
  fit();
  return { update: fit };
};
