import type { Prefs } from '$lib/types';

declare global {
  namespace App {
    interface Error {
      message: string;
    }
    interface Locals {
      prefs: Prefs;
    }
  }
}

export {};
