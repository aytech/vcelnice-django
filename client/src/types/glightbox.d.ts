// GLightbox 3.3.1's root declarations contain an invalid Payload<T> index and omit
// external slides. Type only the distribution API we use, without skipLibCheck.
declare module 'glightbox/dist/js/glightbox.min.js' {
  interface Slide {
    href: string
    type: 'image' | 'external'
    title: string
    alt?: string
    width?: string
    height?: string
  }

  interface Options {
    elements: Slide[]
    openEffect: 'none'
    closeEffect: 'none'
    slideEffect: 'none'
    preload: boolean
    keyboardNavigation: boolean
    moreLength: number
  }

  interface Instance {
    setElements(slides: Slide[]): void
    openAt(index: number): void
    on(event: 'open' | 'close' | 'slide_after_load' | 'slide_changed', callback: () => void): void
    getActiveSlide(): HTMLElement | null
    prevSlide(): void
    nextSlide(): void
    close(): void
    destroy(): void
  }

  export default function GLightbox(options: Options): Instance
}
