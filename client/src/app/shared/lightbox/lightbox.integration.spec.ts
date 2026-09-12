import { ErrorHandler } from '@angular/core'
import { TestBed } from '@angular/core/testing'
import { NavigationStart, Router } from '@angular/router'
import { Subject } from 'rxjs'
import { Photo } from '@interfaces'
import { LightboxService } from './lightbox.service'

describe('LightboxService with GLightbox', () => {
  let service: LightboxService
  let navigation: Subject<NavigationStart>
  let errorHandler: jasmine.SpyObj<ErrorHandler>
  let host: HTMLDivElement
  let trigger: HTMLAnchorElement

  beforeEach(() => {
    navigation = new Subject<NavigationStart>()
    errorHandler = jasmine.createSpyObj<ErrorHandler>('ErrorHandler', ['handleError'])
    spyOn(window, 'open').and.returnValue(null)
    TestBed.configureTestingModule({
      providers: [
        LightboxService,
        { provide: Router, useValue: { events: navigation } },
        { provide: ErrorHandler, useValue: errorHandler }
      ]
    })
    service = TestBed.inject(LightboxService)
    host = document.createElement('div')
    trigger = document.createElement('a')
    trigger.href = '/assets/images/default.png'
    trigger.textContent = 'Otevřít fotogalerii'
    host.appendChild(trigger)
    document.body.appendChild(host)
  })

  afterEach(async () => {
    TestBed.resetTestingModule()
    await Promise.resolve()
    navigation.complete()
    host.remove()
  })

  it('opens the eighth preview, advances to the ninth photo and fully closes with Escape', async () => {
    const photos: Photo[] = Array.from({ length: 12 }, (_, index) => photo(index + 1))
    trigger.focus()
    openPhotos(photos, 7)

    const eighthSlide = await loadedSlide(photos[7].caption)
    const dialog = document.getElementById('glightbox-body') as HTMLElement
    const nextButton = dialog.querySelector<HTMLButtonElement>('.gnext') as HTMLButtonElement

    expect(dialog.querySelectorAll('.gslide').length).toBe(12)
    expect(eighthSlide.inert).toBeFalse()
    expect(host.inert).toBeTrue()
    expect(getComputedStyle(dialog).position).toBe('fixed')
    expect(nextButton.getClientRects().length).toBeGreaterThan(0)

    nextButton.click()
    const ninthSlide = await loadedSlide(photos[8].caption)

    expect(ninthSlide).not.toBe(eighthSlide)
    expect(eighthSlide.inert).toBeTrue()
    expect(eighthSlide.getAttribute('aria-hidden')).toBe('true')
    expect(ninthSlide.getAttribute('aria-hidden')).toBe('false')

    dialog.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Escape', bubbles: true, cancelable: true
    }))
    await waitFor(() => document.getElementById('glightbox-body') ? null : true,
      'the lightbox to close')
    await Promise.resolve()

    expect(document.querySelector('.glightbox-container')).toBeNull()
    expect(document.querySelector('.gcss-styles')).toBeNull()
    expect(document.documentElement.classList.contains('glightbox-open')).toBeFalse()
    expect(document.body.classList.contains('glightbox-open')).toBeFalse()
    expect(document.body.classList.contains('gscrollbar-fixer')).toBeFalse()
    expect(host.inert).toBeFalse()
    expect(host.hasAttribute('aria-hidden')).toBeFalse()
    expect(document.activeElement).toBe(trigger)
    expect(errorHandler.handleError).not.toHaveBeenCalled()
  })

  it('renders an untrusted caption as plain text in the real gallery', async () => {
    const caption = '<img src=x onerror=void(0)> & med'
    openPhotos([{ ...photo(1), caption }], 0)

    const activeSlide = await loadedSlide(caption)
    const title = activeSlide.querySelector<HTMLElement>('.gslide-title') as HTMLElement
    const image = activeSlide.querySelector<HTMLImageElement>('.gslide-image img') as HTMLImageElement

    expect(title.textContent).toBe(caption)
    expect(title.querySelector('img')).toBeNull()
    expect(title.children.length).toBe(0)
    expect(image.alt).toBe(caption)
    expect(image.naturalWidth).toBeGreaterThan(0)
    expect(errorHandler.handleError).not.toHaveBeenCalled()
  })

  function photo(id: number): Photo {
    return {
      id,
      image: '/assets/images/default.png',
      caption: `Fotografie ${id}`,
      thumb: '/assets/images/default.png'
    }
  }

  function openPhotos(photos: readonly Photo[], index: number): void {
    trigger.addEventListener('click', event => service.openPhotos(event, photos, index), { once: true })
    trigger.dispatchEvent(new MouseEvent('click', { button: 0, bubbles: true, cancelable: true }))
  }

  function loadedSlide(caption: string): Promise<HTMLElement> {
    return waitFor(() => {
      const slide = document.querySelector<HTMLElement>('#glightbox-body .gslide.current')
      const image = slide?.querySelector<HTMLImageElement>('.gslide-image img')
      return slide && !slide.inert && slide.querySelector('.gslide-title')?.textContent === caption &&
        image?.complete && image.naturalWidth > 0 ? slide : null
    }, `the gallery image with caption ${caption}`)
  }

  function waitFor<T>(read: () => T | null, description: string): Promise<T> {
    return new Promise((resolve, reject) => {
      const observer = new MutationObserver(check)
      const timeout = window.setTimeout(() => {
        cleanup()
        reject(new Error(`Timed out waiting for ${description}`))
      }, 3000)

      function cleanup(): void {
        observer.disconnect()
        document.removeEventListener('load', check, true)
        window.clearTimeout(timeout)
      }

      function check(): void {
        const result = read()
        if (result === null) return
        cleanup()
        resolve(result)
      }

      observer.observe(document.body, { childList: true, subtree: true, attributes: true, characterData: true })
      document.addEventListener('load', check, true)
      check()
    })
  }
})
