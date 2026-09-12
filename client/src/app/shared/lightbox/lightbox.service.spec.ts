import { ErrorHandler } from '@angular/core'
import { TestBed } from '@angular/core/testing'
import { NavigationStart, Router } from '@angular/router'
import { Subject } from 'rxjs'
import { Photo, Video } from '@interfaces'
import { LIGHTBOX_LOADER, LightboxFactory, LightboxInstance } from './lightbox-loader'
import { LightboxService } from './lightbox.service'

describe('LightboxService', () => {
  const photos: Photo[] = Array.from({ length: 12 }, (_, index) => ({
    id: index + 1,
    image: `/media/photo-${index + 1}.jpg`,
    caption: `Fotografie ${index + 1}`,
    thumb: `/media/photo-${index + 1}-thumb.jpg`
  }))
  const video: Video = {
    youtube_id: 'dQw4w9WgXcQ',
    caption: 'Včely & med',
    description: null,
    thumb: null
  }

  let service: LightboxService
  let load: jasmine.Spy<() => Promise<LightboxFactory>>
  let factory: jasmine.Spy<LightboxFactory>
  let lightbox: jasmine.SpyObj<LightboxInstance>
  let errorHandler: jasmine.SpyObj<ErrorHandler>
  let navigation: Subject<NavigationStart>
  let host: HTMLDivElement
  let trigger: HTMLAnchorElement
  let dialog: HTMLDivElement
  let slide: HTMLDivElement
  let closeButton: HTMLButtonElement
  let nextButton: HTMLButtonElement

  beforeEach(() => {
    navigation = new Subject<NavigationStart>()
    host = document.createElement('div')
    trigger = document.createElement('a')
    trigger.href = '/media/photo-1.jpg'
    trigger.textContent = 'Otevřít'
    host.appendChild(trigger)
    document.body.appendChild(host)

    dialog = document.createElement('div')
    dialog.id = 'glightbox-body'
    dialog.setAttribute('role', 'dialog')
    closeButton = document.createElement('button')
    closeButton.className = 'gclose'
    const previousButton = document.createElement('button')
    previousButton.className = 'gprev'
    nextButton = document.createElement('button')
    nextButton.className = 'gnext'
    slide = document.createElement('div')
    slide.className = 'gslide'
    dialog.append(closeButton, previousButton, nextButton, slide)

    lightbox = jasmine.createSpyObj<LightboxInstance>('GLightbox', [
      'on', 'setElements', 'openAt', 'getActiveSlide', 'close', 'destroy', 'prevSlide', 'nextSlide'
    ])
    lightbox.getActiveSlide.and.returnValue(slide)
    lightbox.openAt.and.callFake(() => {
      document.body.appendChild(dialog)
      emit('open')
    })
    lightbox.close.and.callFake(() => {
      emit('close')
      dialog.remove()
    })
    lightbox.destroy.and.callFake(() => dialog.remove())
    factory = jasmine.createSpy<LightboxFactory>('GLightbox factory').and.returnValue(lightbox)
    load = jasmine.createSpy<() => Promise<LightboxFactory>>('GLightbox loader')
      .and.returnValue(Promise.resolve(factory))
    errorHandler = jasmine.createSpyObj<ErrorHandler>('ErrorHandler', ['handleError'])

    TestBed.configureTestingModule({
      providers: [
        LightboxService,
        { provide: LIGHTBOX_LOADER, useValue: load },
        { provide: Router, useValue: { events: navigation } },
        { provide: ErrorHandler, useValue: errorHandler }
      ]
    })
    service = TestBed.inject(LightboxService)
  })

  afterEach(() => {
    TestBed.resetTestingModule()
    navigation.complete()
    dialog.remove()
    host.remove()
  })

  it('loads on a plain click and opens every photo at the selected index', async () => {
    const event = new MouseEvent('click', { button: 0, cancelable: true })

    expect(load).not.toHaveBeenCalled()
    service.openPhotos(event, photos, 5)
    await settle()

    expect(event.defaultPrevented).toBeTrue()
    expect(load).toHaveBeenCalledTimes(1)
    expect(factory).toHaveBeenCalledWith(jasmine.objectContaining({
      elements: [], preload: false, keyboardNavigation: false
    }))
    expect(lightbox.setElements).toHaveBeenCalledOnceWith(photos.map(photo => ({
      href: new URL(photo.image, document.baseURI).href,
      type: 'image',
      title: photo.caption,
      alt: photo.caption
    })))
    expect(lightbox.openAt).toHaveBeenCalledOnceWith(5)
  })

  it('preserves modified and non-left clicks for every kind of link', async () => {
    const options: MouseEventInit[] = [
      { ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { altKey: true },
      { button: 1 }, { button: 2 }
    ]
    const actions = [
      (event: MouseEvent) => service.openPhotos(event, photos, 0),
      (event: MouseEvent) => service.openVideo(event, video),
      (event: MouseEvent) => service.openMap(event)
    ]

    for (const action of actions) {
      for (const option of options) {
        const event = new MouseEvent('click', { button: 0, cancelable: true, ...option })
        action(event)
        expect(event.defaultPrevented).toBeFalse()
      }
      const prevented = new MouseEvent('click', { button: 0, cancelable: true })
      prevented.preventDefault()
      action(prevented)
    }
    await settle()

    expect(load).not.toHaveBeenCalled()
  })

  it('escapes captions at the third-party HTML boundary while preserving image alt text', async () => {
    const caption = '<img src=x onerror=alert(1)>& med'
    service.openPhotos(new MouseEvent('click'), [{ ...photos[0], caption }], 0)
    await settle()

    expect(lightbox.setElements).toHaveBeenCalledOnceWith([jasmine.objectContaining({
      title: '&lt;img src=x onerror=alert(1)&gt;&amp; med',
      alt: caption
    })])
  })

  it('does not intercept unsafe photo URLs or invalid starting indices', async () => {
    for (const image of ['javascript:alert(1)', 'data:image/svg+xml,<svg/>', 'file:///secret.jpg']) {
      const event = new MouseEvent('click', { cancelable: true })
      service.openPhotos(event, [photos[0], { ...photos[1], image }], 0)
      expect(event.defaultPrevented).toBeFalse()
    }
    for (const index of [-1, 1.5, photos.length, Number.NaN]) {
      const event = new MouseEvent('click', { cancelable: true })
      service.openPhotos(event, photos, index)
      expect(event.defaultPrevented).toBeFalse()
    }
    await settle()

    expect(load).not.toHaveBeenCalled()
  })

  it('opens one YouTube privacy-enhanced iframe and supplies its accessible media attributes', async () => {
    const frame = document.createElement('iframe')
    slide.appendChild(frame)

    service.openVideo(new MouseEvent('click'), video)
    await settle()

    expect(lightbox.setElements).toHaveBeenCalledOnceWith([jasmine.objectContaining({
      href: 'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ?rel=0&autoplay=1',
      type: 'external',
      title: 'Včely &amp; med'
    })])
    expect(lightbox.openAt).toHaveBeenCalledOnceWith(0)
    expect(frame.title).toBe(video.caption)
    expect(frame.referrerPolicy).toBe('strict-origin-when-cross-origin')
    expect(frame.allow).toContain('autoplay')
    expect(frame.allowFullscreen).toBeTrue()

    frame.removeAttribute('title')
    emit('slide_after_load')
    expect(frame.title).toBe(video.caption)
  })

  it('does not intercept malformed YouTube identifiers', async () => {
    for (const youtube_id of ['short', 'https://youtu.be/dQw4w9WgXcQ', '../bad?id=x']) {
      const event = new MouseEvent('click', { cancelable: true })
      service.openVideo(event, { ...video, youtube_id })
      expect(event.defaultPrevented).toBeFalse()
    }
    await settle()

    expect(load).not.toHaveBeenCalled()
  })

  it('uses an embeddable map URL rather than the normal Google Maps search URL', async () => {
    service.openMap(new MouseEvent('click'))
    await settle()

    expect(lightbox.setElements).toHaveBeenCalledOnceWith([jasmine.objectContaining({
      href: 'https://maps.google.com/maps?q=Riegrova%20376%2C%20252%2019%20Rudn%C3%A1&output=embed',
      type: 'external',
      title: 'Riegrova 376, 252 19 Rudná'
    })])
    expect(dialog.getAttribute('aria-label')).toBe('Mapa – Včelnice Rudná')
  })

  it('discards a pending lazy load after SPA navigation', async () => {
    let resolveLoad!: (factory: LightboxFactory) => void
    load.and.returnValue(new Promise(resolve => { resolveLoad = resolve }))

    service.openPhotos(new MouseEvent('click'), photos, 0)
    navigation.next(new NavigationStart(1, '/privacy'))
    resolveLoad(factory)
    await settle()

    expect(factory).not.toHaveBeenCalled()
    expect(document.getElementById('glightbox-body')).toBeNull()
  })

  it('restores focus and the original inert state after the visitor closes the dialog', async () => {
    const alreadyInert = document.createElement('div')
    alreadyInert.inert = true
    document.body.appendChild(alreadyInert)
    try {
      trigger.focus()
      clickTrigger(event => service.openPhotos(event, photos, 0))
      await settle()

      expect(document.activeElement).toBe(closeButton)
      expect(host.inert).toBeTrue()
      expect(dialog.getAttribute('aria-modal')).toBe('true')
      expect(closeButton.getAttribute('aria-label')).toBe('Zavřít')
      expect(nextButton.getAttribute('aria-label')).toBe('Další fotografie')

      lightbox.close()
      await settle()

      expect(document.activeElement).toBe(trigger)
      expect(host.inert).toBeFalse()
      expect(alreadyInert.inert).toBeTrue()
      expect(lightbox.destroy).toHaveBeenCalledTimes(1)
    } finally {
      alreadyInert.remove()
    }
  })

  it('cleans up an open dialog and embedded media on navigation without restoring old-page focus', async () => {
    const frame = document.createElement('iframe')
    const image = document.createElement('img')
    const imageLoaded = jasmine.createSpy('GLightbox image load')
    image.addEventListener('load', imageLoaded)
    frame.onload = jasmine.createSpy('iframe load')
    image.onload = jasmine.createSpy('image load')
    slide.append(frame, image)
    clickTrigger(event => service.openMap(event))
    await settle()
    const focus = spyOn(trigger, 'focus')

    navigation.next(new NavigationStart(1, '/privacy'))
    await settle()

    expect(lightbox.destroy).toHaveBeenCalledTimes(1)
    expect(document.getElementById('glightbox-body')).toBeNull()
    expect(frame.onload).toBeNull()
    expect(image.onload).toBeNull()
    image.dispatchEvent(new Event('load'))
    expect(imageLoaded).not.toHaveBeenCalled()
    expect(frame.src).toBe('about:blank')
    expect(host.inert).toBeFalse()
    expect(focus).not.toHaveBeenCalled()

    dialog.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }))
    expect(lightbox.nextSlide).not.toHaveBeenCalled()
  })

  it('supports gallery keyboard navigation, wraps focus and closes with Escape', async () => {
    service.openPhotos(new MouseEvent('click'), photos, 0)
    await settle()

    dialog.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }))
    dialog.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowLeft', bubbles: true }))
    expect(lightbox.nextSlide).toHaveBeenCalledTimes(1)
    expect(lightbox.prevSlide).toHaveBeenCalledTimes(1)

    nextButton.focus()
    nextButton.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', bubbles: true, cancelable: true }))
    expect(document.activeElement).toBe(closeButton)
    closeButton.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Tab', shiftKey: true, bubbles: true, cancelable: true
    }))
    expect(document.activeElement).toBe(nextButton)

    dialog.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    await settle()
    expect(lightbox.close).toHaveBeenCalledTimes(1)
  })

  it('hides inactive slides from keyboard and screen-reader navigation', async () => {
    const inactive = document.createElement('div')
    inactive.className = 'gslide'
    dialog.appendChild(inactive)
    service.openPhotos(new MouseEvent('click'), photos, 0)
    await settle()

    expect(inactive.inert).toBeTrue()
    expect(inactive.getAttribute('aria-hidden')).toBe('true')
    expect(slide.inert).toBeFalse()
    expect(slide.getAttribute('aria-hidden')).toBe('false')
    lightbox.getActiveSlide.and.returnValue(inactive)
    emit('slide_changed')
    await settle()
    expect(inactive.inert).toBeFalse()
    expect(slide.inert).toBeTrue()
  })

  it('shows a labelled local placeholder if a full-size photo cannot load', async () => {
    const image = document.createElement('img')
    const title = document.createElement('h4')
    title.className = 'gslide-title'
    title.textContent = 'Včelnice'
    slide.append(image, title)
    service.openPhotos(new MouseEvent('click'), photos, 0)
    await settle()

    image.dispatchEvent(new Event('error'))

    expect(image.getAttribute('src')).toBe('/assets/images/default.png')
    expect(image.alt).toBe('Fotografii se nepodařilo načíst.')
    expect(title.textContent).toContain('Fotografii se nepodařilo načíst.')
  })

  it('reports a lazy-import failure and follows the original safe link', async () => {
    const error = new Error('Lightbox chunk failed to load')
    load.and.callFake(() => Promise.reject(error))
    const open = spyOn(window, 'open').and.returnValue(null)

    clickTrigger(event => service.openPhotos(event, photos, 0))
    await settle()

    expect(errorHandler.handleError).toHaveBeenCalledOnceWith(error)
    expect(open).toHaveBeenCalledOnceWith(trigger.href, '_self', 'noopener')
    expect(factory).not.toHaveBeenCalled()
  })

  function emit(name: string): void {
    const callback = lightbox.on.calls.allArgs().find(([event]) => event === name)?.[1]
    if (!callback) throw new Error(`No lightbox handler registered for ${name}`)
    callback()
  }

  function clickTrigger(action: (event: MouseEvent) => void): void {
    trigger.addEventListener('click', event => action(event), { once: true })
    trigger.dispatchEvent(new MouseEvent('click', { button: 0, bubbles: true, cancelable: true }))
  }

  async function settle(): Promise<void> {
    await Promise.resolve()
    await Promise.resolve()
  }
})
