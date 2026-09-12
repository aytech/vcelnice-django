import { InjectionToken } from '@angular/core'
import type GLightbox from 'glightbox/dist/js/glightbox.min.js'

export type LightboxFactory = typeof GLightbox
export type LightboxInstance = ReturnType<LightboxFactory>

// Keep browser-only library code out of initial rendering and make it replaceable in tests.
export const LIGHTBOX_LOADER = new InjectionToken<() => Promise<LightboxFactory>>('LIGHTBOX_LOADER', {
  providedIn: 'root',
  factory: () => () => import('glightbox/dist/js/glightbox.min.js').then(module => module.default)
})
