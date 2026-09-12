import { DOCUMENT } from '@angular/common'
import { DestroyRef, ErrorHandler, Injectable, inject } from '@angular/core'
import { takeUntilDestroyed } from '@angular/core/rxjs-interop'
import { NavigationStart, Router } from '@angular/router'
import { Photo, Video } from '@interfaces'
import { LIGHTBOX_LOADER, LightboxInstance } from './lightbox-loader'

// The bundled GLightbox declarations omit its supported external (iframe) slide type.
interface LightboxSlide {
  href: string
  type: 'image' | 'external'
  title: string
  alt?: string
  width?: string
  height?: string
}

@Injectable({ providedIn: 'root' })
export class LightboxService {
  private readonly document = inject(DOCUMENT)
  private readonly load = inject(LIGHTBOX_LOADER)
  private readonly errorHandler = inject(ErrorHandler)
  private readonly destroyRef = inject(DestroyRef)
  private active?: LightboxInstance
  private release?: (restoreFocus?: boolean) => void
  private request = 0

  constructor() {
    inject(Router).events.pipe(takeUntilDestroyed()).subscribe(event => {
      if (event instanceof NavigationStart) this.close(false)
    })
    this.destroyRef.onDestroy(() => this.close(false))
  }

  openPhotos(event: MouseEvent, photos: readonly Photo[], index: number): void {
    if (!this.isPlainClick(event) || !Number.isInteger(index) || !photos[index]) return

    const slides = photos.map(photo => ({
      href: this.mediaUrl(photo.image),
      type: 'image' as const,
      title: this.escapeText(photo.caption),
      alt: photo.caption
    }))
    // Leave the original link untouched if backend data contains an unsafe URL.
    if (slides.some(slide => !slide.href)) return
    this.open(event, slides, index, 'Fotogalerie')
  }

  openVideo(event: MouseEvent, video: Video): void {
    if (!this.isPlainClick(event) || !/^[a-zA-Z0-9_-]{11}$/.test(video.youtube_id)) return
    this.open(event, [{
      href: `https://www.youtube-nocookie.com/embed/${video.youtube_id}?rel=0&autoplay=1`,
      type: 'external',
      title: this.escapeText(video.caption),
      width: '960px',
      height: 'min(54vw, 540px, 70vh)'
    }], 0, video.caption || 'Video')
  }

  openMap(event: MouseEvent): void {
    if (!this.isPlainClick(event)) return
    this.open(event, [{
      href: 'https://maps.google.com/maps?q=Riegrova%20376%2C%20252%2019%20Rudn%C3%A1&output=embed',
      type: 'external',
      title: 'Riegrova 376, 252 19 Rudná',
      width: '1000px',
      height: '70vh'
    }], 0, 'Mapa – Včelnice Rudná')
  }

  private isPlainClick(event: MouseEvent): boolean {
    return !event.defaultPrevented && event.button === 0 &&
      !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey
  }

  private mediaUrl(value: string): string {
    try {
      const url = new URL(value, this.document.baseURI)
      return ['http:', 'https:'].includes(url.protocol) ? url.href : ''
    } catch {
      return ''
    }
  }

  private escapeText(value: string): string {
    const element = this.document.createElement('span')
    element.textContent = value
    return element.innerHTML
  }

  private open(event: MouseEvent, slides: LightboxSlide[], index: number, label: string): void {
    event.preventDefault()
    const trigger = event.currentTarget as HTMLAnchorElement | null
    this.close(false)
    const request = this.request
    void this.load().then(factory => {
      if (request !== this.request || this.destroyRef.destroyed) return
      const lightbox = factory({
        elements: [],
        openEffect: 'none',
        closeEffect: 'none',
        slideEffect: 'none',
        preload: false,
        keyboardNavigation: false,
        moreLength: 0
      })
      this.active = lightbox
      lightbox.on('open', () => this.prepareDialog(lightbox, trigger, label))
      lightbox.on('slide_after_load', () => this.prepareMedia(lightbox, label))
      lightbox.on('slide_changed', () => queueMicrotask(() => {
        if (this.active === lightbox) this.prepareMedia(lightbox, label)
      }))
      lightbox.on('close', () => {
        this.release?.()
        this.release = undefined
        if (this.active === lightbox) this.active = undefined
        // GLightbox finishes resetting state after emitting its close event.
        queueMicrotask(() => lightbox.destroy())
      })
      lightbox.setElements(slides)
      lightbox.openAt(index)
    }).catch(error => {
      if (request !== this.request || this.destroyRef.destroyed) return
      this.close(false)
      this.errorHandler.handleError(error)
      // A failed lazy chunk must not leave the visitor with a dead link.
      if (trigger && this.mediaUrl(trigger.href)) {
        this.document.defaultView?.open(trigger.href, '_self', 'noopener')
      }
    })
  }

  private prepareMedia(lightbox: LightboxInstance, label: string): void {
    const activeSlide = lightbox.getActiveSlide()
    this.document.querySelectorAll<HTMLElement>('#glightbox-body .gslide').forEach(slide => {
      slide.inert = slide !== activeSlide
      slide.setAttribute('aria-hidden', String(slide !== activeSlide))
    })
    const frame = activeSlide?.querySelector('iframe')
    if (!frame) return
    frame.title = label
    frame.referrerPolicy = 'strict-origin-when-cross-origin'
    frame.allow = 'autoplay; encrypted-media; fullscreen; picture-in-picture'
    frame.allowFullscreen = true
  }

  private prepareDialog(lightbox: LightboxInstance, trigger: HTMLAnchorElement | null, label: string): void {
    const dialog = this.document.getElementById('glightbox-body')
    if (!dialog) return
    dialog.setAttribute('aria-label', label)
    dialog.setAttribute('aria-modal', 'true')
    const controls = { '.gclose': 'Zavřít', '.gprev': 'Předchozí fotografie', '.gnext': 'Další fotografie' }
    for (const [selector, title] of Object.entries(controls)) {
      const button = dialog.querySelector<HTMLButtonElement>(selector)
      button?.setAttribute('aria-label', title)
      button?.setAttribute('title', title)
    }
    this.prepareMedia(lightbox, label)

    const background = Array.from(this.document.body.children)
      .filter((element): element is HTMLElement => element instanceof HTMLElement && element !== dialog)
      .map(element => ({ element, inert: element.inert }))
    background.forEach(({ element }) => { element.inert = true })

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault()
        lightbox.close()
      } else if (event.key === 'Tab') {
        const focusable = Array.from(dialog.querySelectorAll<HTMLElement>(
          'button:not(:disabled), a[href], iframe, input, select, textarea, [tabindex="0"]'
        )).filter(element => element.getClientRects().length && !element.classList.contains('disabled'))
        if (!focusable.length) return
        const current = focusable.indexOf(this.document.activeElement as HTMLElement)
        const next = current < 0 ? (event.shiftKey ? focusable.length - 1 : 0) :
          (current + (event.shiftKey ? -1 : 1) + focusable.length) % focusable.length
        event.preventDefault()
        focusable[next].focus()
      } else if ((event.key === 'ArrowLeft' || event.key === 'ArrowRight') &&
        !(event.target instanceof HTMLElement && event.target.matches('input, textarea, select, [contenteditable="true"]'))) {
        event.preventDefault()
        event.key === 'ArrowLeft' ? lightbox.prevSlide() : lightbox.nextSlide()
      }
    }
    dialog.addEventListener('keydown', onKeyDown)
    const onImageError = (event: Event) => {
      const image = event.target
      if (!(image instanceof HTMLImageElement) || image.dataset.lightboxFallback) return
      image.dataset.lightboxFallback = 'true'
      const message = 'Fotografii se nepodařilo načíst.'
      image.alt = message
      const title = image.closest('.gslide')?.querySelector('.gslide-title')
      if (title) title.textContent = `${title.textContent} — ${message}`
      // A bundled placeholder allows GLightbox to finish its normal loading lifecycle.
      image.src = '/assets/images/default.png'
    }
    dialog.addEventListener('error', onImageError, true)
    this.release = (restoreFocus = true) => {
      dialog.removeEventListener('keydown', onKeyDown)
      dialog.removeEventListener('error', onImageError, true)
      dialog.querySelectorAll('img, iframe').forEach(element => {
        // Cancel late load callbacks and stop embedded media even during early close.
        const media = element as HTMLImageElement | HTMLIFrameElement
        media.onload = null
        if (media instanceof HTMLIFrameElement) {
          media.src = 'about:blank'
        } else {
          // GLightbox uses addEventListener, not the onload property, for images.
          media.addEventListener('load', event => event.stopImmediatePropagation(), { capture: true, once: true })
          media.removeAttribute('srcset')
          media.removeAttribute('src')
        }
      })
      background.forEach(({ element, inert }) => { element.inert = inert })
      if (restoreFocus && trigger?.isConnected) trigger.focus({ preventScroll: true })
    }
    dialog.querySelector<HTMLButtonElement>('.gclose')?.focus({ preventScroll: true })
  }

  private close(restoreFocus: boolean): void {
    this.request++
    const lightbox = this.active
    // Release before removal to cancel pending iframe/image load handlers.
    this.release?.(restoreFocus)
    this.release = undefined
    lightbox?.destroy()
    this.active = undefined
  }
}
